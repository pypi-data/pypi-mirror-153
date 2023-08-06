import argparse
import logging
import re
import sys
import time
from pathlib import Path

import keras
import numpy as np
import tensorflow as tf
from icecream import ic
from skimage import io

from scalingtheunet.models.simple_unet import Mish, mish_activation
from scalingtheunet.utils.file_system import load_d2_to_d3
from scalingtheunet.utils.stdlogging import initStream
from scalingtheunet.utils.utils import crop_center_3d, do_post_processing, mpire_3d_rotation, pad_3d, ray_3d_rotation

log = logging.getLogger(__name__)
save_predictions = False


def main(
    model_path: Path, test_data_path: Path, out_file_path: Path, processing_list: list, batch_size: int, print_timing=True
):
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

    with strategy.scope():
        custom_objects = {"Mish": Mish, "mish_activation": mish_activation}
        # At loading time, register the custom objects with a `custom_object_scope`:
        model = keras.models.load_model(str(model_path), custom_objects=custom_objects, compile=False)
        # num_classes is the channel dim of the last layer
        num_classes = model.output.shape[-1]
        log.info("Number of classes: {}".format(num_classes))
        # get number of down blocks
        for idx, l in enumerate(model.layers):
            if "latent" in l.name:
                break
        last_down_layer = model.layers[idx - 1]
        num_down_blocks = re.findall(r"\d+", last_down_layer.name.split("_")[0])
        num_down_blocks = int(num_down_blocks[0]) + 1
        log.info("Number of down block: {}".format(num_down_blocks))

        prediction = keras.layers.Activation(activation="softmax")(model.layers[-2].output)
        model = keras.models.Model(inputs=[model.input], outputs=[prediction])

    #############################
    # Load data and run testing
    #############################
    start_time = time.time()

    log.info(f"Loading: {test_data_path}")
    if test_data_path.is_dir():
        img_3d_raw = load_d2_to_d3(test_data_path)
    else:
        if test_data_path.suffix == ".npy":
            img_3d_raw = np.load(str(test_data_path))
        else:
            img_3d_raw = io.imread(str(test_data_path))

    img_3d_raw_shape = img_3d_raw.shape

    logits_3d_sum = np.zeros(img_3d_raw_shape + (num_classes,), dtype=np.float32)
    total_directions = 0
    for direction_list, rotation_axis in processing_list:
        log.info(f"Directions and axis: {direction_list}, {rotation_axis}")
        block_time = time.time()
        if len(rotation_axis) > 0:
            log.debug(f"rotating vol around axis: {rotation_axis}")
            log.info(f"Image size befor rotation: {img_3d_raw.shape}")
            img_3d = mpire_3d_rotation(img_3d_raw.copy(), rotation_axis=rotation_axis, rotation_angel=45, reshape=True)
            log.info(f"Image size after rotation: {img_3d.shape}")
            batchsize = batch_size // 2
        else:
            batchsize = batch_size
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
        img_3d = img_3d - 0.5

        global_batch_size = batchsize * strategy.num_replicas_in_sync
        img_3d_shape_before_padding = img_3d.shape
        padding_size = 2 ** num_down_blocks
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
            log.info(f"Image size befor transpose {img_3d_tmp.shape}")
            if direction == 0:
                padding = (img_3d_shape_before_padding[0], pad_img_size[1], pad_img_size[2])
            elif direction == 1:
                img_3d_tmp = np.transpose(img_3d_tmp, axes=(1, 0, 2))
                log.info(f"Image size after transpose {img_3d_tmp.shape}")
                padding = (img_3d_shape_before_padding[1], pad_img_size[0], pad_img_size[2])
            else:
                img_3d_tmp = np.transpose(img_3d_tmp, axes=(2, 0, 1))
                log.info(f"Image size after transpose {img_3d_tmp.shape}")
                padding = (img_3d_shape_before_padding[2], pad_img_size[0], pad_img_size[1])
            img_3d_tmp = pad_3d(img_3d_tmp, padding)
            log.info(f"Image size after padding: {img_3d_tmp.shape}")

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
            logits_3d = np.zeros(img_3d_tmp.shape + (num_classes,), dtype=np.float32)
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
                logits_3d_out = np.zeros(img_3d_raw_shape + (num_classes,), dtype=np.float32)
                for channel in range(num_classes):
                    logits_3d_out[..., channel] = mpire_3d_rotation(
                        logits_3d[..., channel].copy(),
                        rotation_axis=rotation_axis,
                        rotation_angel=-45,
                        reshape=True,
                        output_dim=img_3d_raw_shape,
                    )
            else:
                logits_3d_out = logits_3d.copy()

            del logits_3d
            if save_predictions:
                np.save(
                    str(out_file_path).replace(".npy", f"_slice-ax-{direction}_rot{''.join(map(str,rotation_axis))}_.npy"),
                    logits_3d_out,
                )
            logits_3d_sum += logits_3d_out

    log.info("Finished prediction!")
    # raw classification result
    logits_3d_all = (np.argmax(logits_3d_sum / total_directions, axis=-1)).astype(np.uint8)
    # opening+closing only on label cor screw and screw
    block_time = time.time()
    logits_3d_all = do_post_processing(logits_3d_all)
    if print_timing:
        log.debug("PostProcessing BlockTime --- %s seconds ---" % (time.time() - block_time))

    if not out_file_path.parent.is_dir():
        out_file_path.parent.mkdir()
    log.info(f"Saving img to: {str(out_file_path)}")
    np.save(str(out_file_path), logits_3d_all)
    log.debug("Total Time --- %s seconds ---" % (time.time() - start_time))
