import logging
import os
from functools import partial
from typing import Callable, Tuple

import hydra
import numpy as np
import tensorflow as tf
from albumentations import BasicTransform, Compose
from omegaconf import DictConfig

log = logging.getLogger(__name__)

AUTOTUNE = tf.data.experimental.AUTOTUNE
aug_comp_train: Callable = ...
aug_comp_val: Callable = ...

# TODO: rename file to be more generic
class HZGDataset:
    def __init__(
        self,
        train_list_file,
        val_list_file,
        image_size,
        image_size_val,
        image_channels,
        num_classes,
        class_names,
        batch_size,
        data_aug: DictConfig,
        main_config: DictConfig,
        num_worker: int,
    ):
        self.config = main_config
        self.num_classes = num_classes
        self.class_names = class_names

        self.image_shape_training: Tuple[int, int, int] = (image_size, image_size, image_channels)
        self.mask_shape_training: Tuple[int, int, int] = (image_size, image_size, num_classes)

        self.image_shape_validation: Tuple[int, int, int] = (image_size_val, image_size_val, image_channels)
        self.mask_shape_validation: Tuple[int, int, int] = (image_size_val, image_size_val, num_classes)

        self.global_batch_size = batch_size * num_worker
        self.BUFFER_SIZE = 1000

        # loading file path from text file
        self._img_train_paths, self._mask_train_paths = self.load_data(train_list_file, do_shuffle=True)
        self.train_data_size = len(self._img_train_paths)

        self._img_val_paths, self._mask_val_paths = self.load_data(val_list_file, do_shuffle=False)
        self._img_val_paths, self._mask_val_paths = (self._img_val_paths[::20], self._mask_val_paths[::20])
        self.val_data_size = len(self._img_val_paths)

        aug_comp_training: list[BasicTransform] = []
        aug_comp_validation: list[BasicTransform] = []
        if data_aug:
            if data_aug.get("training"):
                for _, da_conf in data_aug.training.items():
                    if "_target_" in da_conf:
                        log.info(f"Instantiating training data transformation <{da_conf._target_}>")
                        aug_comp_training.append(hydra.utils.instantiate(da_conf))

            if data_aug.get("validation"):
                for _, da_conf in data_aug.validation.items():
                    if "_target_" in da_conf:
                        log.info(f"Instantiating validation data transformation <{da_conf._target_}>")
                        aug_comp_validation.append(hydra.utils.instantiate(da_conf))

            for da_key, da_conf in data_aug.items():
                if "_target_" in da_conf:
                    log.info(f"Instantiating transformation for train/val <{da_conf._target_}>")
                    transformation = hydra.utils.instantiate(da_conf)
                    aug_comp_training.append(transformation)
                    aug_comp_validation.append(transformation)

        self.set_aug_train(aug_comp_training)
        self.set_aug_val(aug_comp_validation)

        # self.ds_train = self.get_dataset(img_train_path, mask_train_path, phase="training")
        # self.ds_val = self.get_dataset(img_val_path, mask_val_path, phase="validation")

    def load_data(self, list_file, do_shuffle) -> (np.array, np.array):
        x_data: list = []
        y_data: list = []
        with open(os.path.join(self.config.data_dir, list_file), "r") as file:
            for line in file.readlines():
                [folder, file_name] = line.split()
                x_data.append(os.path.join(self.config.data_dir, folder, "images", file_name))
                y_data.append(os.path.join(self.config.data_dir, folder, "masks", file_name))
        log.info("Dataset %s has %d samples.", list_file, len(x_data))
        # shuffle data
        if do_shuffle:
            indexes = np.arange(len(x_data))
            np.random.shuffle(indexes)
            x_data = np.array(x_data)[indexes]
            y_data = np.array(y_data)[indexes]

        return x_data, y_data

    def get_dataset(self, phase) -> tf.data.Dataset:
        if phase == "training":
            img_paths, mask_paths = self._img_train_paths, self._mask_train_paths
            img_shape = self.image_shape_training
            mask_shape = self.mask_shape_training
        elif phase == "validation":
            img_paths, mask_paths = self._img_val_paths, self._mask_val_paths
            img_shape = self.image_shape_validation
            mask_shape = self.mask_shape_validation
        else:
            raise ValueError

        dataset = tf.data.Dataset.from_tensor_slices((img_paths, mask_paths))
        if phase == "training":
            dataset = dataset.shuffle(len(img_paths), reshuffle_each_iteration=True, seed=42)
        dataset = dataset.map(load_data_fn, num_parallel_calls=AUTOTUNE).prefetch(buffer_size=AUTOTUNE)
        if phase == "training":
            process_data_fn = process_data_train_fn
        elif phase == "validation":
            process_data_fn = process_data_val_fn
        else:
            raise ValueError
        dataset = dataset.map(
            partial(
                process_data_fn,
                num_classes=self.num_classes,
            ),
            num_parallel_calls=AUTOTUNE,
        )

        dataset = dataset.map(
            partial(set_shapes, img_shape=img_shape, mask_shape=mask_shape), num_parallel_calls=AUTOTUNE
        ).prefetch(buffer_size=AUTOTUNE)

        if phase == "training":
            dataset = dataset.repeat()
        dataset = dataset.batch(self.global_batch_size, drop_remainder=True)
        dataset = dataset.prefetch(buffer_size=AUTOTUNE)

        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        dataset = dataset.with_options(options)
        return dataset

    def set_aug_train(self, aug_comp):
        global aug_comp_train
        aug_comp_train = Compose(aug_comp)

    def set_aug_val(self, aug_comp):
        global aug_comp_val
        aug_comp_val = Compose(aug_comp)


def load_data_fn(image, mask) -> (tf.Tensor, tf.Tensor):
    image, mask = tf.numpy_function(func=read_data_fn, inp=[image, mask], Tout=[tf.float32, tf.uint8])
    return image, mask


def read_data_fn(image: str, mask: str) -> (tf.Tensor, tf.Tensor):
    image = np.load(image)[:, :, np.newaxis].astype(np.float32)
    mask = np.load(mask)[:, :, np.newaxis].astype(np.uint8)
    return image, mask


def process_data_train_fn(image, mask, num_classes) -> (tf.Tensor, tf.Tensor):
    aug_img, aug_mask = tf.numpy_function(func=aug_train_fn, inp=[image, mask], Tout=[tf.float32, tf.uint8])
    aug_mask_one_hot = tf.one_hot(aug_mask, depth=num_classes)
    return aug_img, aug_mask_one_hot


def aug_train_fn(image: np.array, mask: np.array) -> (tf.Tensor, tf.Tensor):
    global aug_comp_train
    data = {"image": image, "mask": mask}
    aug_data = aug_comp_train(**data)
    return tf.cast(aug_data["image"], tf.float32), tf.cast(aug_data["mask"][..., 0], tf.uint8)


def process_data_val_fn(image, mask, num_classes) -> (tf.Tensor, tf.Tensor):
    aug_img, aug_mask = tf.numpy_function(func=aug_val_fn, inp=[image, mask], Tout=[tf.float32, tf.uint8])
    aug_mask_one_hot = tf.one_hot(aug_mask, depth=num_classes)
    return aug_img, aug_mask_one_hot


def aug_val_fn(image: np.array, mask: np.array) -> (tf.Tensor, tf.Tensor):
    global aug_comp_val
    data = {"image": image, "mask": mask}
    aug_data = aug_comp_val(**data)
    return tf.cast(aug_data["image"], tf.float32), tf.cast(aug_data["mask"][..., 0], tf.uint8)


def set_shapes(image, mask, img_shape=(512, 512, 1), mask_shape=(512, 512, 4)) -> (tf.Tensor, tf.Tensor):
    image.set_shape(img_shape)
    mask.set_shape(mask_shape)
    return image, mask
