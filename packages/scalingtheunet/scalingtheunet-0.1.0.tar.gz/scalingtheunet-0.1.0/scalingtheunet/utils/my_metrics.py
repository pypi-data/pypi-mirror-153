import warnings
from typing import Callable, List

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K


def seg_metric(
    class_idx: int = None,
    num_classes: int = None,
    flag_soft: bool = True,
    name: str = "avr",
    include_background: bool = True,
    squared_pred: bool = False,
    jaccard: bool = False,
    smooth_nr: float = 1.0,
    smooth_dr: float = 1.0,
) -> Callable[[tf.Tensor, tf.Tensor], tf.Tensor]:
    """
    Args:
        name:
        class_idx:
        include_background: if False, channel index 0 (background category) is excluded from the calculation.
        squared_pred: use squared versions of targets and predictions in the denominator or not.
        jaccard: compute Jaccard Index (soft IoU) instead of dice or not.
        smooth_nr: a small constant added to the numerator to avoid zero.
        smooth_dr: a small constant added to the denominator to avoid nan.

    Raises:
    """

    def metric(
        y_true: tf.Tensor,
        y_pred: tf.Tensor,
    ) -> tf.Tensor:
        """
        Args:
            input: the shape should be BH[WD]N, where N is the number of classes.
            target: the shape should be BH[WD]N, where N is the number of classes.

        Raises:
            AssertionError: When input and target (after one hot transform if setted)
                have different shapes.
            ValueError: When ``self.reduction`` is not one of ["mean", "sum", "none"].

        """
        y_pred = K.softmax(y_pred, axis=-1)
        if not flag_soft:
            # get one-hot encoded masks from y_pred (true mask should already be one-hot)
            y_pred = K.one_hot(K.argmax(y_pred), num_classes)

        if class_idx is not None:
            # if class_idx, removing all other channels
            # slice without lossing dim
            y_true = y_true[..., None, class_idx]
            y_pred = y_pred[..., None, class_idx]

        n_pred_ch = y_pred.shape[-1]
        if not include_background:
            if n_pred_ch == 1:
                warnings.warn("single channel prediction, `include_background=False` ignored.")
            else:
                # if skipping background, removing first channel
                y_true = y_true[..., 1:]
                y_pred = y_pred[..., 1:]

        # reducing only spatial dimensions (not batch nor channels)
        reduce_axis: List[int] = list(np.arange(1, len(y_pred.shape) - 1))
        intersection = K.sum(y_true * y_pred, axis=reduce_axis)

        if squared_pred:
            y_true = K.pow(y_true, 2)
            y_pred = K.pow(y_pred, 2)

        ground_o = K.sum(y_true, axis=reduce_axis)
        pred_o = K.sum(y_pred, axis=reduce_axis)

        denominator = ground_o + pred_o

        if jaccard:
            denominator = 2.0 * (denominator - intersection)

        f: tf.Tensor = (2.0 * intersection + smooth_nr) / (denominator + smooth_dr)

        # reducing only channel dimensions (not batch)
        out = K.mean(f, axis=[1])
        return out

    name_string = f"soft_"
    if not flag_soft:
        name_string = f"hard_"

    if jaccard:
        name_string += f"iou"
    else:
        name_string += f"dice"

    if class_idx is not None:
        name_string += f"_{name}"
    else:
        if not include_background:
            name_string += f"_noBG_{name}"
        else:
            name_string += f"_wBG_{name}"
    metric.__name__ = name_string  # Set name used to log metric
    return metric


def bacc_metric(
    class_idx: int = None,
    name: str = "avr",
    include_background: bool = True,
    num_classes: int = 2,
    smooth_nr: float = 1e-5,
    smooth_dr: float = 1e-5,
) -> Callable[[tf.Tensor, tf.Tensor], tf.Tensor]:
    """
    Args:
        name:
        class_idx:
        include_background: if False, channel index 0 (background category) is excluded from the calculation.
        squared_pred: use squared vers  ions of targets and predictions in the denominator or not.
        jaccard: compute Jaccard Index (soft IoU) instead of dice or not.
        smooth_nr: a small constant added to the numerator to avoid zero.
        smooth_dr: a small constant added to the denominator to avoid nan.

    Raises:
    """

    def metric(
        y_true: tf.Tensor,
        y_pred: tf.Tensor,
    ) -> tf.Tensor:
        """
        Args:
            input: the shape should be BH[WD]N, where N is the number of classes.
            target: the shape should be BH[WD]N, where N is the number of classes.

        Raises:
            AssertionError: When input and target (after one hot transform if setted)
                have different shapes.
            ValueError: When ``self.reduction`` is not one of ["mean", "sum", "none"].

        """
        y_pred = K.softmax(y_pred, axis=-1)
        y_pred = K.one_hot(K.argmax(y_pred), num_classes)

        if class_idx is not None:
            # if class_idx, removing all other channels
            # slice without lossing dim
            y_true = y_true[..., None, class_idx]
            y_pred = y_pred[..., None, class_idx]

        n_pred_ch = y_pred.shape[-1]
        if not include_background:
            if n_pred_ch == 1:
                warnings.warn("single channel prediction, `include_background=False` ignored.")
            else:
                # if skipping background, removing first channel
                y_true = y_true[..., 1:]
                y_pred = y_pred[..., 1:]
        # reducing only spatial dimensions (not batch nor channels)
        reduce_axis: List[int] = list(np.arange(1, len(y_pred.shape) - 1))
        tp = K.sum(y_true * y_pred, axis=reduce_axis)
        fp = K.sum(y_pred * (1 - y_true), axis=reduce_axis)
        fn = K.sum((1 - y_pred) * y_true, axis=reduce_axis)
        tn = K.sum((1 - y_pred) * (1 - y_true), axis=reduce_axis)

        nominator = 2 * tp * tn + tp * fp + tn * fn
        denominator = 2.0 * (tp + fn) * (tn + fp)

        f: tf.Tensor = (nominator + smooth_nr) / (denominator + smooth_dr)

        # reducing only channel dimensions (not batch)
        out = K.mean(f, axis=[1])
        return out

    name_string = f"bacc"

    if class_idx is not None:
        name_string += f"_{name}"
    else:
        if not include_background:
            name_string += f"_noBG_{name}"
        else:
            name_string += f"_wBG_{name}"
    metric.__name__ = name_string  # Set name used to log metric
    return metric
