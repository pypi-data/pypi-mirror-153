import logging
import os
import platform
import sys
from typing import Optional

from omegaconf import DictConfig

try:
    import mlflow

    use_mlflow = True
except:
    use_mlflow = False

try:
    import wandb

    use_wandb = True
except:
    use_wandb = False

import hydra
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import mixed_precision
from tensorflow.keras.callbacks import Callback

# our imports
from scalingtheunet.models import simple_unet
from scalingtheunet.utils import my_hydra as my_hydra_utils
from scalingtheunet.utils.my_losses import CESegLoss, SegLoss
from scalingtheunet.utils.my_metrics import bacc_metric, seg_metric
from scalingtheunet.utils.stdlogging import initStream

log = logging.getLogger(__name__)
if not sys.stdout.isatty():
    initStream()
    VERBOSE = 2
else:
    VERBOSE = 1


def create_model(config: DictConfig, strategy):
    #########################
    # Initialize network
    #########################
    """
    Specifically, this function implements single-machine
    multi-GPU data parallelism. It works in the following way:

    - Divide the model's input(s) into multiple sub-batches.
    - Apply a model copy on each sub-batch. Every model copy
      is executed on a dedicated GPU.
    - Concatenate the results (on CPU) into one big batch.

    E.g. if your `batch_size` is 64 and you use `gpus=2`,
    then we will divide the input into 2 sub-batches of 32 samples,
    process each sub-batch on one GPU, then return the full
    batch of 64 processed samples.
    """
    with strategy.scope():
        model = simple_unet.custom_unet(
            (None, None, config.datamodule.image_channels),
            num_classes=config.datamodule.num_classes,
            dropout=config.model.dropout,
            dropout_conv=config.model.dropout_conv,
            filters=config.model.filters,
            regularization_factor_l1=config.model.regularization_factor_l1,
            regularization_factor_l2=config.model.regularization_factor_l2,
            use_norm=config.model.use_norm,
            activation=config.model.activation,
            num_layers=config.model.num_layers,
            kernel_size=tuple(config.model.kernel_size),
            output_activation=config.model.output_activation,
            dropout_type=config.model.dropout_type,
            layer_order=config.model.layer_order,
        )
        model.summary(print_fn=log.info)

        #########################
        # Compile
        #########################
        from_logits = True if config.model.output_activation == "linear" else False
        if config.trainer.loss_function == "ce":
            loss_fn = keras.losses.CategoricalCrossentropy(from_logits=from_logits)
        elif config.trainer.loss_function == "dice":
            loss_fn = SegLoss(include_background=False, from_logits=from_logits)
        elif config.trainer.loss_function == "logDice":
            loss_fn = SegLoss(include_background=False, log_dice=True, from_logits=from_logits)
        elif config.trainer.loss_function == "dice_bg":
            loss_fn = SegLoss(include_background=True, from_logits=from_logits)
        elif config.trainer.loss_function == "dice_ce":
            loss_fn = CESegLoss(include_background=False, log_dice=False, from_logits=from_logits)
        elif config.trainer.loss_function == "logDice_ce":
            loss_fn = CESegLoss(include_background=False, log_dice=True, from_logits=from_logits)
        else:
            raise NotImplemented(f"Your loss <{config.trainer.loss_function}> is not implemented!")

        metric_fns = [
            seg_metric(include_background=False),
            # seg_metric(include_background=False, flag_soft=False, num_classes=config.datamodule.num_classes),
            # seg_metric(include_background=False, jaccard=True, flag_soft=False, num_classes=config.datamodule.num_classes),
            bacc_metric(include_background=False, num_classes=config.datamodule.num_classes),
        ]

        log.info(f"Instantiating optimizer <{config.trainer.optimizer._target_}>")
        optimizer_fn = hydra.utils.instantiate(config.trainer.optimizer)

    model.compile(
        optimizer=optimizer_fn,
        loss=loss_fn,
        metrics=metric_fns,
    )

    return model


def create_callbacks(config, train_batch, val_batch):
    # Init loggers
    logger: list[Callback] = []
    if "logger" in config:
        for lg_key, lg_conf in config.logger.items():
            if "image_logger" in lg_key:
                log.info(f"Instantiating logger <{lg_conf._target_}>")
                logger.append(
                    hydra.utils.instantiate(
                        lg_conf,
                        sample_batch=train_batch,
                        phase="train",
                        _recursive_=False,
                    )
                )
                logger.append(
                    hydra.utils.instantiate(
                        lg_conf,
                        sample_batch=val_batch,
                        phase="val",
                        _recursive_=False,
                    )
                )
                continue

            if "wandb_init" in lg_key and use_wandb:
                log.info(
                    f"Instantiating wandb run: <entity={lg_conf.user}>, <project={lg_conf.project}>, <name={lg_conf.name}>",
                )
                wandb.tensorboard.patch(root_logdir=config.logger.tensorboard.get("log_dir"))
                wandb.init(entity=lg_conf.user, project=lg_conf.project, name=lg_conf.name, sync_tensorboard=True)

            if "_target_" in lg_conf:
                log.info(f"Instantiating logger <{lg_conf._target_}>")
                logger.append(hydra.utils.instantiate(lg_conf))

    callbacks: list[Callback] = []
    if "callbacks" in config:
        for _, cb_conf in config.callbacks.items():
            if "_target_" in cb_conf:
                log.info(f"Instantiating callback <{cb_conf._target_}>")
                callbacks.append(hydra.utils.instantiate(cb_conf))

    callbacks = callbacks + logger

    if config.trainer.get("lr_scheduler"):
        log.info(f"Instantiating lr scheduler <{config.trainer.lr_scheduler._target_}>")
        callbacks.append(hydra.utils.instantiate(config.trainer.lr_scheduler))
    return callbacks


def save_params_to_mlflow(config):
    # data_aug
    keys = ["RandomResizedCrop_p", "Flip_p", "Rotate_p", "ElasticTransform_p", "RandomBrightnessContrast_p"]
    for k in keys:
        mlflow.log_param(k, config["data_aug"][k])

    # model
    keys = [
        "image_size",
        "image_size_val",
        "num_layers",
        "filters",
        "regularization_factor_l1",
        "regularization_factor_l2",
        "dropout",
        "dropout_conv",
        "activation",
        "dropout",
        "dropout_conv",
        "kernel_size",
        "use_norm",
    ]
    for k in keys:
        mlflow.log_param(k, config["model_params"][k])

    # loss_params
    keys = ["loss"]
    for k in keys:
        mlflow.log_param(k, config["loss_params"][k])

    # optimizer_params
    keys = ["optimizer_name", "learning_rate", "amsgrad", "use_mixed_precision"]
    for k in keys:
        mlflow.log_param(k, config["optimizer_params"][k])
    mlflow.log_artifact(os.path.join(args_dict["experiment_path"], os.path.basename(args_dict["config_file"])))


def train(config: DictConfig) -> Optional[float]:
    # check devices
    physical_devices = tf.config.list_physical_devices("GPU")
    if config.trainer.get("num_gpus") >= 1 and config.trainer.get("num_gpus") > len(physical_devices):
        raise ValueError(f"Did not find enough GPUs. Reduce the number of GPUs to use!")
    if config.trainer.get("num_gpus") == 0 and len(physical_devices) > 0:
        # hiding all GPUs!
        tf.config.set_visible_devices([], "GPU")
    elif 0 < config.trainer.get("num_gpus") < len(physical_devices):
        gpus_to_hide = len(physical_devices) - config.trainer.get("num_gpus")
        # hiding some GPUs!
        tf.config.set_visible_devices(physical_devices[gpus_to_hide:], "GPU")
    else:
        # use all GPUs
        config.trainer.num_gpus = len(physical_devices)

    # TF usually allocates all memory of the GPU
    visible_devices = tf.config.list_physical_devices("GPU")
    if visible_devices:
        visible_devices = tf.config.list_physical_devices("GPU")
        for gpu in visible_devices:
            tf.config.experimental.set_memory_growth(gpu, True)

    strategy = tf.distribute.MirroredStrategy()
    num_worker = strategy.num_replicas_in_sync
    log.info("Number of worker devices: {}".format(num_worker))

    if config.get("use_mixed_precision"):
        policy = mixed_precision.Policy("mixed_float16")
        mixed_precision.set_global_policy(policy)

    if config.get("mlflow_dir") and use_mlflow:
        if platform.system() == "Windows":
            mlflow.set_tracking_uri(f"file:/{config.mlflow_dir}")
        else:
            mlflow.set_tracking_uri(f"file://{config.mlflow_dir}")
        mlflow.set_experiment("U-Net Segmentation - training")
        experiment = mlflow.get_experiment_by_name("U-Net Segmentation - training")

    #############################
    # Doing data stuff
    #############################
    log.info(f"Instantiating datamodule <{config.datamodule._target_}>")
    datamodule = hydra.utils.instantiate(
        config.datamodule,
        main_config=config,
        num_worker=num_worker,
        _convert_=None,
        _recursive_=False,
    )
    training_generator = datamodule.get_dataset("training")
    valid_genarator = datamodule.get_dataset("validation")

    # extract 1 batch from both dataset
    train_batch = next(iter(training_generator))
    val_batch = next(iter(valid_genarator))

    #########################
    # Initialize model
    #########################
    log.info("Instantiating model")
    model = create_model(config, strategy)

    #########################
    # Callbacks for model training
    #########################
    callbacks = create_callbacks(config, train_batch, val_batch)

    #########################
    # Start training of model
    #########################
    steps_per_epoch = config.trainer.iterations_pro_epoch // datamodule.global_batch_size

    total_training_samples = config.trainer.epochs * datamodule.train_data_size
    effective_epochs = (total_training_samples // config.trainer.iterations_pro_epoch) + 1
    validation_freq = config.trainer.validation_freq

    log.info(f"new effective total epochs: {effective_epochs}")
    log.info(f"iteration for each effective epoch: {steps_per_epoch}")
    log.info(f"global batch size: {datamodule.global_batch_size}")

    if config.get("mlflow_dir") and use_mlflow:
        with mlflow.start_run(run_name=f"{config.name}_{config.current_time}", experiment_id=experiment.experiment_id):
            save_params_to_mlflow(config)
            mlflow.tensorflow.autolog()
            history = model.fit(
                training_generator,
                epochs=effective_epochs,
                steps_per_epoch=steps_per_epoch,
                verbose=VERBOSE,
                validation_data=valid_genarator,
                validation_freq=validation_freq,
                callbacks=callbacks,
                use_multiprocessing=False,
                shuffle=False,
            )
    else:
        history = model.fit(
            training_generator,
            epochs=effective_epochs,
            steps_per_epoch=steps_per_epoch,
            verbose=VERBOSE,
            validation_data=valid_genarator,
            validation_freq=validation_freq,
            callbacks=callbacks,
            use_multiprocessing=False,
            shuffle=False,
        )

    if config.get("print_history"):
        my_hydra_utils.print_history(history.history)
    # save last model!
    model.save(os.path.join(os.getcwd(), "last_model.hdf5"))
