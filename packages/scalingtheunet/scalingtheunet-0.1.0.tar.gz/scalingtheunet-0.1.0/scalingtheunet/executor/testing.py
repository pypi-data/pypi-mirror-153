import logging
import os
import socket
import time
from pathlib import Path

import flatdict
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import tensorflow as tf
import torch
from keras import layers, models, utils
from monai.metrics import compute_meandice, get_confusion_matrix
from monai.metrics.confusion_matrix import compute_confusion_matrix_metric
from omegaconf import DictConfig, OmegaConf, open_dict
from skimage import io

from scalingtheunet.models.simple_unet import Mish, mish_activation
from scalingtheunet.utils.file_system import load_d2_to_d3
from scalingtheunet.utils.utils import (
    crop_center_3d,
    do_post_processing,
    mpire_3d_rotation,
    numba_confusion_matrix,
    pad_3d,
    plot_cm,
    plot_imgs,
)

log = logging.getLogger(__name__)
print_timing = True

AXIS_ZERO = [
    ([0], []),
]

AXIS_ONE = [
    ([0], []),
]

AXIS_TWO = [
    ([0], []),
]

THREE_AXES_LIST = [
    ([0, 1, 2], []),
]

NINE_AXES_LIST = [([1, 2], (2, 1)), ([0, 2], (2, 0)), ([0, 1, 2], []), ([0, 1], (1, 0))]


def my_eval(class_names, mask_3d_onehot, prediction_3d_onehot, name, folder, out_path, num_classes, **kwargs):
    start_time = time.time()
    conf_mat = numba_confusion_matrix(
        np.argmax(mask_3d_onehot, axis=-1).flatten(), np.argmax(prediction_3d_onehot, axis=-1).flatten(), int(num_classes)
    )
    log.info("Conv mat calc --- %s seconds ---" % (time.time() - start_time))
    log.info(np.array2string(conf_mat))

    plot_cm(conf_mat, class_names, fig_path=os.path.join(out_path, "figs", f"{folder}_{name}_ml-Conf-Mat.png"))
    mlflow.log_artifact(os.path.join(out_path, "figs", f"{folder}_{name}_ml-Conf-Mat.png"))
    kwargs["average_conf_mat"] += conf_mat

    prediction_3d_onehot = torch.tensor(np.transpose(prediction_3d_onehot[np.newaxis, :, :, :, :], axes=(0, 4, 1, 2, 3)))
    mask_3d_onehot = torch.tensor(np.transpose(mask_3d_onehot[np.newaxis, :, :, :, :], axes=(0, 4, 1, 2, 3)))
    start_time = time.time()
    dice_per_class = compute_meandice(prediction_3d_onehot, mask_3d_onehot, include_background=True).numpy()
    log.info("dice_per_class calc --- %s seconds ---" % (time.time() - start_time))
    for i, label_name in enumerate(class_names):
        log.info(f"{folder}_{name}_{label_name}-Dice: \t {dice_per_class[0][i]}")
        mlflow.log_metric(f"{folder}_{name}_{label_name}-Dice", dice_per_class[0][i])
    kwargs["average_dice"] += dice_per_class

    # Multi-Class confusion matrix
    start_time = time.time()
    # tp, fp, tn, fn
    confusion_matrix_per_class = get_confusion_matrix(prediction_3d_onehot, mask_3d_onehot, include_background=True)
    log.info("confusion_matrix_per_class calc --- %s seconds ---" % (time.time() - start_time))
    for i, label_name in enumerate(class_names):
        log.info(
            {
                f"{folder}_{name}_{label_name}-TP": confusion_matrix_per_class.numpy()[0, i, 0],
                f"{folder}_{name}_{label_name}-FP": confusion_matrix_per_class.numpy()[0, i, 1],
                f"{folder}_{name}_{label_name}-TN": confusion_matrix_per_class.numpy()[0, i, 2],
                f"{folder}_{name}_{label_name}-FN": confusion_matrix_per_class.numpy()[0, i, 3],
            }
        )
    kwargs["average_conf_mat_per_class"] += confusion_matrix_per_class.numpy()

    confusion_matrix_metric = {}
    # threat score = IoU
    for m_name in kwargs["average_conf_mat_metrics"].keys():
        log.info(m_name)
        confusion_matrix_metric[m_name] = compute_confusion_matrix_metric(
            metric_name=m_name, confusion_matrix=confusion_matrix_per_class
        )
        # log.info(np.array2string(confusion_matrix_metric[m_name].numpy()))
        for i, label_name in enumerate(class_names):
            log.info(f"{folder}_{name}_{label_name}-{m_name}: \t {confusion_matrix_metric[m_name].numpy()[0, i]}")
        # mlflow.log_metric(f"{folder}_{name}_{label_name}-{m_name}", confusion_matrix_metric[m_name].numpy()[0, i])
        kwargs["average_conf_mat_metrics"][m_name] += confusion_matrix_metric[m_name].numpy()

    return kwargs


def save_params_to_mlflow(exp_config: DictConfig, eval_config: str):
    hparams = {}

    hparams["testing_data"] = eval_config.testing_data
    hparams["eval_name"] = eval_config.eval_name
    hparams["eval_type"] = eval_config.eval_type
    hparams["eval_axes"] = eval_config.eval_axes
    hparams["do_postprocessing"] = eval_config.do_postprocessing

    # choose which parts of hydra config will be saved to loggers
    hparams["trainer"] = OmegaConf.to_container(exp_config["trainer"], resolve=True)
    hparams["model"] = OmegaConf.to_container(exp_config["model"], resolve=True)
    hparams["datamodule"] = OmegaConf.to_container(exp_config["datamodule"], resolve=True)
    if exp_config.get("seed"):
        hparams["seed"] = exp_config["seed"]

    # flatten nested dicts
    hparams = dict(flatdict.FlatDict(hparams, delimiter="/"))

    for k, v in hparams.items():
        mlflow.log_param(k, v)


def save_example_images(img_3d, mask_3d, logits_3d_all, image_path, num_images=9):
    slice_step = img_3d.shape[0] // num_images
    for slice in range(0, img_3d.shape[0], slice_step):
        out_figure = plot_imgs(
            img_3d[slice : slice + 2, :, :],
            mask_3d[slice : slice + 2, :, :],
            logits_3d_all[slice : slice + 2, :, :],
            nm_img_to_plot=2,
            save_imgs=True,
            show_imgs=False,
        )
        out_figure.savefig(f"{image_path}-axis0_{slice}.png")
        mlflow.log_artifact(f"{image_path}-axis0_{slice}.png")
        plt.close()
    for slice in range(0, img_3d.shape[1], slice_step):
        out_figure = plot_imgs(
            np.transpose(img_3d[:, slice : slice + 2, :], axes=(1, 0, 2)),
            np.transpose(mask_3d[:, slice : slice + 2, :], axes=(1, 0, 2)),
            np.transpose(logits_3d_all[:, slice : slice + 2, :], axes=(1, 0, 2)),
            nm_img_to_plot=2,
            save_imgs=True,
            show_imgs=False,
        )
        out_figure.savefig(f"{image_path}-axis1_{slice}.png")
        mlflow.log_artifact(f"{image_path}-axis1_{slice}.png")
        plt.close()


def init_mlflow(config):
    mlflow.set_tracking_uri(f"file://{str(f'{config.mlflow_dir}')}")
    if config.testing_data == "training":
        mlflow.set_experiment("U-Net Segmentation - training data")
        experiment = mlflow.get_experiment_by_name("U-Net Segmentation - training data")
    elif config.testing_data == "validation":
        mlflow.set_experiment("U-Net Segmentation - validation data")
        experiment = mlflow.get_experiment_by_name("U-Net Segmentation - validation data")
    else:
        if config.get("do_eval"):
            mlflow.set_experiment("U-Net Segmentation - publication")
            experiment = mlflow.get_experiment_by_name("U-Net Segmentation - publication")
        else:
            mlflow.set_experiment("U-Net Segmentation - only calculation")
            experiment = mlflow.get_experiment_by_name("U-Net Segmentation - only calculation")

    current_experiment = dict(experiment)
    experiment_id = current_experiment["experiment_id"]
    df = mlflow.search_runs([experiment_id], order_by=["metrics.IoU DESC"])
    # get ids by name
    if len(df) > 0:
        old_run_ids = list(df["run_id"][df["tags.mlflow.runName"].str.contains(f"{config.experiment_dir}")])

        for old_run_id in old_run_ids:
            old_run = df[df["run_id"] == old_run_id]
            # check ids for eval type and status
            if (
                (old_run["status"] == "FINISHED").any()
                and (old_run["params.eval_type"] == config.eval_name).any()
                and not config.get("rerun")
            ):
                # found old run but rerun flag was not set
                raise RuntimeError("Found old run!")
            if (old_run["params.eval_type"] == config.eval_name).any():
                # remove old run and start new one
                print(f"Removing run: {old_run_id}")
                mlflow.delete_run(old_run_id)
    return experiment


def run(config):
    def predict_step(inputs):
        predictions = model(inputs, training=False)
        return predictions

    @tf.function
    def distributed_predict_step(dist_inputs):
        per_replica_predictions = strategy.run(predict_step, args=(dist_inputs,))
        return strategy.gather(per_replica_predictions, axis=0)

    physical_devices = tf.config.list_physical_devices("GPU")
    for gpu in physical_devices:
        tf.config.experimental.set_memory_growth(gpu, True)
    strategy = tf.distribute.MirroredStrategy()
    log.info("Number of devices: {}".format(strategy.num_replicas_in_sync))
    if config.eval_type == "soft_voting":
        eval_name = "Average"
    else:
        eval_name = "MV"

    if config.eval_axes == 9:
        processing_list = NINE_AXES_LIST
        eval_name += "_9axes"
    elif config.eval_axes == 3:
        processing_list = THREE_AXES_LIST
        eval_name += "_9axes"
    elif config.eval_axes == 2:
        processing_list = AXIS_TWO
        eval_name += "_2axis"
    elif config.eval_axes == 1:
        processing_list = AXIS_ONE
        eval_name += "_1axis"
    elif config.eval_axes == 0:
        processing_list = AXIS_ZERO
        eval_name += "_0axis"
    else:
        raise NotImplemented("This number of eval axes is not implemented!")

    if config.get("do_postprocessing"):
        eval_name += "_PostProcessing"

    with open_dict(config):
        config.eval_name = eval_name

    # load old config
    experiment_dir = Path(os.getcwd()).absolute()
    exp_config = OmegaConf.load(experiment_dir / "hydra_training" / "config.yaml")

    with strategy.scope():
        custom_objects = {"Mish": Mish, "mish_activation": mish_activation}
        # At loading time, register the custom objects with a `custom_object_scope`:

        model = models.load_model(
            os.path.join(experiment_dir, config.trained_model_name), custom_objects=custom_objects, compile=False
        )
        if exp_config.model.output_activation == "linear":
            prediction = layers.Activation(activation="softmax")(model.layers[-2].output)
        else:
            prediction = model.layers[-1].output
        model = models.Model(inputs=[model.input], outputs=[prediction])

    experiment = init_mlflow(config)

    with mlflow.start_run(run_name=config.experiment_dir, experiment_id=experiment.experiment_id):
        out_path = experiment_dir / "results"
        if not out_path.is_dir():
            out_path.mkdir()
        if not (out_path / "figs").is_dir():
            (out_path / "figs").mkdir()

        mlflow.log_artifact(str(experiment_dir / "hydra_training" / "config.yaml"))
        save_params_to_mlflow(exp_config, config)

        average_conf_mat = np.zeros((exp_config.datamodule.num_classes, exp_config.datamodule.num_classes), dtype=np.int64)
        average_dice = np.zeros((1, exp_config.datamodule.num_classes), dtype=np.float64)
        average_conf_mat_per_class = np.zeros((1, exp_config.datamodule.num_classes, 4), dtype=np.float64)
        conf_mat_metrics_name = [
            "sensitivity",
            "specificity",
            "precision",
            "negative predictive value",
            "miss rate",
            "fall out",
            "false discovery rate",
            "false omission rate",
            "prevalence threshold",
            "threat score",
            "accuracy",
            "balanced accuracy",
            "f1 score",
            "matthews correlation coefficient",
            "fowlkes mallows index",
            "informedness",
            "markedness",
        ]
        average_conf_mat_metrics = {}
        for n in conf_mat_metrics_name:
            average_conf_mat_metrics[n] = np.zeros((1, exp_config.datamodule.num_classes), dtype=np.float64)

        dict_avrg_args = {
            "average_conf_mat": average_conf_mat,
            "average_dice": average_dice,
            "average_conf_mat_per_class": average_conf_mat_per_class,
            "average_conf_mat_metrics": average_conf_mat_metrics,
        }

        #############################
        # Load data and run testing
        #############################
        samples = []
        if config.testing_data == "training":
            log.info(f"Using training data for eval!")
            # TODO: check this function
            with open(os.path.join(exp_config.data_dir, exp_config.datamodule.train_list_file), "r") as file:
                for line in file.readlines():
                    [dir, file_name] = line.split()
                    sample_name = Path(dir).name
                    if sample_name not in samples:
                        samples.append(sample_name)
        elif config.testing_data == "validation":
            log.info(f"Using val data for eval!")
            with open(os.path.join(exp_config.data_dir, exp_config.datamodule.val_list_file), "r") as file:
                for line in file.readlines():
                    [dir, file_name] = line.split()
                    sample_name = Path(dir).name
                    if sample_name not in samples:
                        samples.append(sample_name)
        else:
            log.info(f"Using test data for eval!")
            samples = config.testing_data

        data_dir = Path(exp_config.data_dir) / config.testing_root
        for sample_name in samples:
            start_time = time.time()

            log.info(f"Loading: {str(data_dir / sample_name)}")
            img_3d_raw = np.load(str(data_dir / sample_name / "image" / "volume3d.npy"))

            log.info(f"Img shape: {img_3d_raw.shape}")
            img_3d_raw_shape = img_3d_raw.shape

            # TODO: not sure how to handle this
            # mlflow.log_param("gold_standard", args_dict["gold_standard"])
            # if args_dict["gold_standard"] == "wfHQ":
            #    mask_3d = load_d2_to_d3(data_dir / folder / "mask_HQ")
            # else:
            mask_3d = load_d2_to_d3(str(data_dir / sample_name / "mask" / "mask3d.npy"))

            if not (out_path / f"{sample_name}_{config.eval_name}_raw.tif").is_file() or config.get("rerun"):
                logits_3d_sum = np.zeros(img_3d_raw_shape + (exp_config.datamodule.num_classes,), dtype=np.float32)
                total_directions = 0
                for direction_list, rotation_axis in processing_list:
                    log.info(f"Directions and axis: {direction_list}, {rotation_axis}")
                    block_time = time.time()
                    if len(rotation_axis) > 0:
                        log.debug(f"rotating vol around axis: {rotation_axis}")
                        log.info(f"Image size befor rotation: {img_3d_raw.shape}")
                        img_3d = mpire_3d_rotation(
                            img_3d_raw.copy(), rotation_axis=rotation_axis, rotation_angel=45, reshape=True
                        )
                        log.info(f"Image size after rotation: {img_3d.shape}")
                        batch_size = np.floor(exp_config.datamodule.batch_size / 2)
                    else:
                        batch_size = exp_config.datamodule.batch_size
                        img_3d = img_3d_raw

                    if print_timing:
                        log.debug("Rotation BlockTime --- %s seconds ---" % (time.time() - block_time))

                        # Norm/Clip data
                    log.info(f"Min/max val: {np.min(img_3d)}, {np.max(img_3d)}")
                    p_low, p_high = np.percentile(img_3d, 0.5), np.percentile(img_3d, 99.9)
                    log.info(f"Norm and clip to 0.5%, 99.9% percentile: {p_low}, {p_high}")
                    img_3d = np.clip(img_3d, p_low, p_high)
                    img_3d = (img_3d - np.min(img_3d)) * (1.0 / (np.max(img_3d) - np.min(img_3d)))
                    # center mean
                    if exp_config.datamodule.get("data_aug") and exp_config.datamodule.data_aug.get("norm_data"):
                        img_3d = img_3d - exp_config.datamodule.data_aug.norm_data.mean
                        img_3d = img_3d / exp_config.datamodule.data_aug.norm_data.std

                    global_batch_size = batch_size * strategy.num_replicas_in_sync
                    img_3d_shape_before_padding = img_3d.shape
                    padding_size = 2 ** exp_config.model.num_layers
                    # padding based on unet blocks
                    pad_img_size = (
                        int(np.ceil(img_3d_shape_before_padding[0] / padding_size) * padding_size),
                        int(np.ceil(img_3d_shape_before_padding[1] / padding_size) * padding_size),
                        int(np.ceil(img_3d_shape_before_padding[2] / padding_size) * padding_size),
                    )

                    # convert from 3D to 2D slices (each direction)
                    for direction in direction_list:
                        log.debug(f"Processing slicing axis {direction}")
                        total_directions += 1
                        img_3d_tmp = img_3d.copy()
                        if len(rotation_axis) > 0:
                            file_name = str(
                                out_path / f"{sample_name}_axis{direction}_rotAxis{rotation_axis[0]}{rotation_axis[1]}.tif"
                            )
                        else:
                            file_name = str(out_path / f"{sample_name}_axis{direction}.tif")
                        if not os.path.isfile(file_name) or config.rerun:
                            if direction == 0:
                                padding = (img_3d_shape_before_padding[0], pad_img_size[1], pad_img_size[2])
                            elif direction == 1:
                                img_3d_tmp = np.transpose(img_3d_tmp, axes=(1, 0, 2))
                                padding = (img_3d_shape_before_padding[1], pad_img_size[0], pad_img_size[2])
                            else:
                                img_3d_tmp = np.transpose(img_3d_tmp, axes=(2, 0, 1))
                                padding = (img_3d_shape_before_padding[2], pad_img_size[0], pad_img_size[1])
                            log.debug(f"Padding sample to shape: {padding}")
                            img_3d_tmp = pad_3d(img_3d_tmp, padding)

                            block_time = time.time()
                            # convert to tf dataset
                            img_tf = tf.data.Dataset.from_tensor_slices(img_3d_tmp[..., np.newaxis])
                            log.debug(f"Total 2d slices: {len(img_tf)}")
                            # Wrap data in Dataset objects.
                            img_tf = img_tf.batch(global_batch_size).prefetch(tf.data.experimental.AUTOTUNE)
                            log.debug(f"Total batches: {len(img_tf)}")
                            options = tf.data.Options()
                            options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
                            img_tf = img_tf.with_options(options)
                            img_tf = strategy.experimental_distribute_dataset(img_tf)

                            if print_timing:
                                log.debug("Tf dataset generation BlockTime --- %s seconds ---" % (time.time() - block_time))

                            block_time = time.time()
                            logits_3d = np.zeros(img_3d_tmp.shape + (exp_config.datamodule.num_classes,), dtype=np.float32)
                            start_idx = 0
                            end_idx = 0
                            for dist_inputs in img_tf:
                                predictions = distributed_predict_step(dist_inputs).numpy()
                                end_idx += len(predictions)
                                logits_3d[start_idx:end_idx] = predictions
                                start_idx += len(predictions)
                            del img_3d_tmp
                            del img_tf

                            if direction == 1:
                                logits_3d = np.transpose(logits_3d, axes=(1, 0, 2, 3))
                            elif direction == 2:
                                logits_3d = np.transpose(logits_3d, axes=(1, 2, 0, 3))

                            if print_timing:
                                log.debug("Prediction BlockTime --- %s seconds ---" % (time.time() - block_time))
                            logits_3d = crop_center_3d(logits_3d, img_3d_shape_before_padding)

                            if len(rotation_axis) > 0:
                                logits_3d_out = np.zeros(
                                    img_3d_raw_shape + (exp_config.datamodule.num_classes,), dtype=np.float32
                                )
                                for channel in range(exp_config.datamodule.num_classes):
                                    logits_3d_out[..., channel] = mpire_3d_rotation(
                                        logits_3d[..., channel].copy(),
                                        rotation_axis=rotation_axis,
                                        rotation_angel=-45,
                                        reshape=False,
                                        output_dim=img_3d_raw_shape,
                                    )
                                if config.get("save_logits"):
                                    io.imsave(
                                        str(
                                            out_path
                                            / f"{sample_name}_axis{direction}_rotAxis{rotation_axis[0]}{rotation_axis[1]}.tif"
                                        ),
                                        logits_3d_out,
                                        check_contrast=False,
                                    )
                            else:
                                logits_3d_out = logits_3d.copy()
                                if config.get("save_logits"):
                                    io.imsave(
                                        str(out_path / f"{sample_name}_axis{direction}.tif"),
                                        logits_3d_out,
                                        check_contrast=False,
                                    )
                            del logits_3d

                        else:
                            log.debug("Found logit file and loading it.")
                            logits_3d_out = io.imread(file_name)

                        if config.eval_type == "soft_voting":
                            logits_3d_sum += logits_3d_out
                        elif config.eval_type == "major_voting":
                            logits_3d_out = np.argmax(logits_3d_out, axis=-1).astype(np.uint8)
                            # utils.to_categorical(logits_3d_out, exp_config.datamodule.num_classes, dtype=np.uint8)
                            logits_3d_sum += utils.to_categorical(
                                logits_3d_out, exp_config.datamodule.num_classes, dtype=np.uint8
                            )
                        else:
                            raise NotImplemented("This is not useful!")

                log.info("Finished prediction!")
                # raw classification result
                logits_3d_all = (np.argmax(logits_3d_sum / total_directions, axis=-1)).astype(np.uint8)
                io.imsave(
                    str(out_path / f"{sample_name}_{config.eval_name}_raw.tif"),
                    logits_3d_all,
                    check_contrast=False,
                )
            else:
                log.info("Found raw prediction and loading it.")
                logits_3d_all = io.imread(str(out_path / f"{sample_name}_{config.eval_name}_raw.tif"))

            if config.get("do_eval"):
                img_3d = img_3d_raw.copy()
                # clip for visualize
                img_3d = np.clip(img_3d, np.percentile(img_3d, 0.5), np.percentile(img_3d, 99.9))
                img_3d = (img_3d - np.min(img_3d)) * (1.0 / (np.max(img_3d) - np.min(img_3d)))

                # opening+closing only on label cor screw and screw
                if config.get("do_postprocessing"):
                    block_time = time.time()
                    logits_3d_all = do_post_processing(logits_3d_all)
                    if print_timing:
                        log.debug("PostProcessing BlockTime --- %s seconds ---" % (time.time() - block_time))

                    io.imsave(
                        str(out_path / f"{sample_name}_{config.eval_name}_post.tif"), logits_3d_all, check_contrast=False
                    )

                # calculate results
                log.info("Final metric calculation!")

                dict_avrg_args = my_eval(
                    exp_config.datamodule.class_names,
                    utils.to_categorical(mask_3d, num_classes=exp_config.datamodule.num_classes, dtype=np.uint8),
                    utils.to_categorical(logits_3d_all, num_classes=exp_config.datamodule.num_classes, dtype=np.uint8),
                    name=config.eval_name,
                    folder=sample_name,
                    out_path=str(out_path),
                    num_classes=exp_config.datamodule.num_classes,
                    **dict_avrg_args,
                )

                log.debug("Total Time --- %s seconds ---" % (time.time() - start_time))

                # save example images
                image_path = str(out_path / f"figs/{sample_name}_{config.eval_name}_example")
                save_example_images(img_3d, mask_3d, logits_3d_all, image_path, num_images=9)

        if config.get("do_eval"):
            # Final average results
            conf_mat_metrics_name = [
                "sensitivity",
                "specificity",
                "precision",
                "negative predictive value",
                "miss rate",
                "fall out",
                "false discovery rate",
                "false omission rate",
                "prevalence threshold",
                "threat score",
                "accuracy",
                "balanced accuracy",
                "f1 score",
                "matthews correlation coefficient",
                "fowlkes mallows index",
                "informedness",
                "markedness",
            ]

            log.info("average_conf_mat: ")
            average_conf_mat = average_conf_mat / len(samples)
            log.info(np.array2string(average_conf_mat))
            plot_cm(
                average_conf_mat,
                exp_config.datamodule.class_names,
                fig_path=os.path.join(out_path, "figs", f"Average_{config.eval_name}_ml-Conf-Mat.png"),
            )
            mlflow.log_artifact(os.path.join(out_path, "figs", f"Average_{config.eval_name}_ml-Conf-Mat.png"))

            log.info("average_dice: ")
            average_dice = average_dice / len(samples)
            log.info(f"Average_{config.eval_name}_Dice: \t {np.mean(average_dice[0, 1:])}")
            for i, label_name in enumerate(exp_config.datamodule.class_names):
                log.info(f"Average_{config.eval_name}_{label_name}-Dice: \t {average_dice[0][i]}")

                mlflow.log_metric(f"Dice_{label_name}", np.mean(average_dice[0, i]))
            mlflow.log_metric(f"Dice", np.mean(average_dice[0, 1:]))

            log.info("average_conf_mat_per_class: ")
            average_conf_mat_per_class = average_conf_mat_per_class / len(samples)
            for i, label_name in enumerate(exp_config.datamodule.class_names):
                log.info(
                    {
                        f"Average_{config.eval_name}_{label_name}-TP": average_conf_mat_per_class[0, i, 0],
                        f"Average_{config.eval_name}_{label_name}-FP": average_conf_mat_per_class[0, i, 1],
                        f"Average_{config.eval_name}_{label_name}-TN": average_conf_mat_per_class[0, i, 2],
                        f"Average_{config.eval_name}_{label_name}-FN": average_conf_mat_per_class[0, i, 3],
                    }
                )

            for m_name in average_conf_mat_metrics.keys():
                log.info(f"average {m_name}")
                tmp_result = average_conf_mat_metrics[m_name] / len(samples)

                for i, label_name in enumerate(exp_config.datamodule.class_names):
                    log.info(f"Average_{config.eval_name}_{label_name}-{m_name}: \t {tmp_result[0, i]}")

                if m_name == "threat score":
                    for i, label_name in enumerate(exp_config.datamodule.class_names):
                        mlflow.log_metric(f"IoU_{label_name}", tmp_result[0, i])
                    mlflow.log_metric(f"IoU", np.mean(tmp_result[0, 1:]))

                if m_name == "balanced accuracy":
                    for i, label_name in enumerate(exp_config.datamodule.class_names):
                        mlflow.log_metric(f"BAcc_{label_name}", tmp_result[0, i])
                    mlflow.log_metric(f"BAcc", np.mean(tmp_result[0, 1:]))
