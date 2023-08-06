import logging
import math
import time

import cc3d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ray
import seaborn as sns
from matplotlib.colors import LogNorm
from mpire import WorkerPool
from numba import jit, prange
from scipy import ndimage
from skimage import color
from skimage.morphology import ball, closing, opening

log = logging.getLogger(__name__)

MASK_COLORS = ["red", "green", "blue", "yellow", "magenta", "cyan"]


def plot_imgs(
    org_imgs,
    mask_imgs,
    pred_imgs=None,
    nm_img_to_plot=10,
    figsize=7,
    alpha=0.5,
    save_imgs=False,
    show_imgs=True,
    show_diff_img=True,
):

    if nm_img_to_plot > org_imgs.shape[0]:
        nm_img_to_plot = org_imgs.shape[0]
    im_id = 0
    org_imgs_size = org_imgs.shape[1]

    org_imgs = reshape_arr(org_imgs)
    mask_imgs = reshape_arr(mask_imgs)
    if not (pred_imgs is None):
        cols = 4
        pred_imgs = reshape_arr(pred_imgs)
    else:
        cols = 3

    fig, axes = plt.subplots(nm_img_to_plot, cols, figsize=(cols * figsize, nm_img_to_plot * figsize), squeeze=False)
    axes[0, 0].set_title("original", fontsize=15)
    axes[0, 1].set_title("ground truth", fontsize=15)
    if not (pred_imgs is None):
        axes[0, 2].set_title("prediction", fontsize=15)
        if show_diff_img:
            axes[0, 3].set_title("Diff mask/prediction", fontsize=15)
        else:
            axes[0, 3].set_title("overlay", fontsize=15)
    else:
        axes[0, 2].set_title("overlay", fontsize=15)
    for m in range(0, nm_img_to_plot):
        axes[m, 0].imshow(org_imgs[im_id], cmap=get_cmap(org_imgs))
        axes[m, 0].set_axis_off()
        axes[m, 1].imshow(color.label2rgb(mask_imgs[im_id], bg_label=0), interpolation="nearest", cmap="jet")
        axes[m, 1].set_axis_off()
        if not (pred_imgs is None):
            axes[m, 2].imshow(color.label2rgb(pred_imgs[im_id], bg_label=0), interpolation="nearest", cmap="jet")
            axes[m, 2].set_axis_off()
            if show_diff_img:
                diff_img = (pred_imgs[im_id] != mask_imgs[im_id]).astype(np.int8)
                axes[m, 3].imshow(
                    color.label2rgb(diff_img, org_imgs[im_id], bg_label=0), interpolation="nearest", cmap="jet"
                )
                axes[m, 3].set_axis_off()
            else:
                axes[m, 3].imshow(
                    color.label2rgb(pred_imgs[im_id], org_imgs[im_id], bg_label=0), interpolation="nearest", cmap="jet"
                )
                axes[m, 3].set_axis_off()
        else:
            axes[m, 2].imshow(
                color.label2rgb(mask_imgs[im_id], org_imgs[im_id], bg_label=0), interpolation="nearest", cmap="jet"
            )
            axes[m, 2].set_axis_off()
        im_id += 1
    plt.subplots_adjust(wspace=0.05, hspace=0.1)
    fig.tight_layout()
    if save_imgs:
        return fig
    if show_imgs:
        plt.show()


def reshape_arr(arr):
    if arr.ndim == 3:
        return arr
    elif arr.ndim == 4:
        if arr.shape[3] == 3:
            return arr
        elif arr.shape[3] == 1:
            return arr.reshape(arr.shape[0], arr.shape[1], arr.shape[2])


def get_cmap(arr):
    if arr.ndim == 3:
        return "gray"
    elif arr.ndim == 4:
        if arr.shape[3] == 3:
            return "jet"
        elif arr.shape[3] == 1:
            return "gray"


def crop_center(img, img_shape_crop):
    cropx, cropy = img_shape_crop
    x, y, _ = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[startx : startx + cropx, starty : starty + cropy, :]


def crop_center_3d(img, img_shape_crop):
    if len(img.shape) == 4:
        x, y, z, _ = img.shape
    else:
        x, y, z = img.shape
    list_idxs = []
    for crop_dim, img_dim in zip(img_shape_crop, [x, y, z]):
        start_idx = img_dim // 2 - (crop_dim // 2) if (img_dim // 2 - (crop_dim // 2)) >= 0 else 0
        end_idx = start_idx + crop_dim if (start_idx + crop_dim) < img_dim else img_dim
        list_idxs.append([start_idx, end_idx])

    return img[list_idxs[0][0] : list_idxs[0][1], list_idxs[1][0] : list_idxs[1][1], list_idxs[2][0] : list_idxs[2][1], ...]


def pad_3d(image, new_shape, value=0.0):
    axes_not_pad = len(image.shape) - len(new_shape)

    old_shape = np.array(image.shape[: len(new_shape)])
    new_shape = np.array([max(new_shape[i], old_shape[i]) for i in range(len(new_shape))])

    difference = new_shape - old_shape
    pad_below = difference // 2
    pad_above = difference - pad_below

    pad_list = [list(i) for i in zip(pad_below, pad_above)] + [[0, 0]] * axes_not_pad

    res = np.pad(image, pad_list, "constant", constant_values=value)
    return res


def plot_cm(cm, labels, fig_path, figsize=(10, 10)):
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = f"{float(p):2.1f}%\n{int(c):d}/\n{int(s):d}"
            elif c == 0:
                annot[i, j] = ""
            else:
                annot[i, j] = f"{float(p):2.1f}%\n{int(c):d}"
    cm = pd.DataFrame(cm, index=labels, columns=labels)
    cm.index.name = "Ground Truth"
    cm.columns.name = "Predicted"
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(cm, cmap="YlGnBu", annot=annot, fmt="", ax=ax, square=True, norm=LogNorm(), robust=False)
    plt.savefig(fig_path)
    plt.close()


@jit(nopython=True, parallel=True)
def numba_confusion_matrix(y_true: np.array, y_predict: np.array, num_classes: int):
    x_size = y_true.shape[0]
    conv_mat = np.zeros((num_classes * num_classes), dtype=np.int64)[:]
    for x in prange(x_size):
        tmp = np.zeros((num_classes * num_classes), dtype=np.int64)
        tmp[num_classes * y_true[x] + y_predict[x]] = 1
        conv_mat += tmp
    return conv_mat.reshape((num_classes, num_classes))


def array_slice(a, axis, start, end, step=1):
    return a[(slice(None),) * (axis % a.ndim) + (slice(start, end, step),)]


@ray.remote
def ray_rotation(image, angle, axes, reshape):
    # Do some image processing.
    return ndimage.rotate(image, angle=angle, axes=axes, reshape=reshape, order=1, mode="constant", cval=0.0, prefilter=True)


def img_size_after_rotation(input_shape, direction, rotation_axis, rotation_angle):
    w, h = input_shape[rotation_axis[0]], input_shape[rotation_axis[1]]
    new_w = round(w * math.cos(math.radians(rotation_angle)) + h * math.sin(math.radians(rotation_angle)))
    new_h = round(w * math.sin(math.radians(rotation_angle)) + h * math.cos(math.radians(rotation_angle)))

    new_dims = np.zeros(3, dtype=np.int16)
    new_dims[list(rotation_axis)] = [new_w, new_h]
    new_dims[direction] = input_shape[direction]
    return list(new_dims)


def ray_3d_rotation(img_3d, num_cpus=40, rotation_axis=(2, 1), rotation_angel=-45, reshape=True, output_dim=None):
    slicing_axis = tuple({0, 1, 2} ^ set(rotation_axis))[0]

    log.info("Start Rotation")
    block_time = time.time()
    block_idxs = np.array_split(np.arange(img_3d.shape[slicing_axis]), num_cpus)
    img_3d_rot = ray.get(
        [
            ray_rotation.remote(
                array_slice(img_3d, slicing_axis, block_idxs[i][0], block_idxs[i][-1] + 1),
                rotation_angel,
                rotation_axis,
                reshape=reshape,
            )
            for i in range(num_cpus)
        ]
    )
    log.info("Rotation BlockTime --- %s seconds ---" % (time.time() - block_time))
    block_time = time.time()

    if not output_dim:
        output_dim = img_size_after_rotation(img_3d.shape, slicing_axis, rotation_axis, rotation_angel)
    img_3d_out = np.zeros(output_dim, dtype=np.float32)
    for idx, block_idx in enumerate(block_idxs):
        s = slice(block_idx[0], block_idx[-1] + 1)
        crop_size = np.array([0, 0, 0])
        crop_size[list(rotation_axis)] = (output_dim[rotation_axis[0]], output_dim[rotation_axis[1]])
        crop_size[slicing_axis] = img_3d_rot[idx].shape[slicing_axis]
        if slicing_axis == 0:
            img_3d_out[s, ...] = crop_center_3d(img_3d_rot[idx], crop_size)
        elif slicing_axis == 1:
            img_3d_out[:, s, :] = crop_center_3d(img_3d_rot[idx], crop_size)
        else:
            img_3d_out[..., s] = crop_center_3d(img_3d_rot[idx], crop_size)
    log.info("Saving BlockTime --- %s seconds ---" % (time.time() - block_time))
    return img_3d_out


def mpire_rotation(img, angle, axes, reshape):
    from scipy import ndimage

    # Do some image processing.
    return ndimage.rotate(img, angle=angle, axes=axes, reshape=reshape, order=1, mode="constant", cval=0.0, prefilter=True)


def mpire_3d_rotation(img_3d, rotation_axis, rotation_angel, reshape=True, num_cpus=40, output_dim=None):
    slicing_axis = tuple({0, 1, 2} ^ set(rotation_axis))[0]

    log.info("Start Rotation")
    block_time = time.time()
    block_idxs = np.array_split(np.arange(img_3d.shape[slicing_axis]), num_cpus)

    iterable_of_args = [
        (
            array_slice(img_3d, slicing_axis, block_idxs[idx][0], block_idxs[idx][-1] + 1),
            rotation_angel,
            rotation_axis,
            reshape,
        )
        for idx in range(num_cpus)
    ]
    log.info(f"Img size: {img_3d.shape}")
    log.info(f"Slice size: {iterable_of_args[0][0].shape}")
    with WorkerPool(n_jobs=num_cpus, start_method="fork") as pool:
        img_3d_rot = pool.map(
            mpire_rotation,
            iterable_of_args,
            iterable_len=num_cpus,
            concatenate_numpy_output=False,
        )
    log.info(f"img_3d_rot size: {len(img_3d_rot)}; {img_3d_rot[0].shape}")
    log.info("Rotation BlockTime --- %s seconds ---" % (time.time() - block_time))
    block_time = time.time()

    if not output_dim:
        output_dim = img_size_after_rotation(img_3d.shape, slicing_axis, rotation_axis, rotation_angel)
    log.info(f"output_dim: {output_dim}")
    img_3d_out = np.zeros(output_dim, dtype=np.float32)
    for idx, block_idx in enumerate(block_idxs):
        s = slice(block_idx[0], block_idx[-1] + 1)
        crop_size = np.array([0, 0, 0])
        crop_size[list(rotation_axis)] = (output_dim[rotation_axis[0]], output_dim[rotation_axis[1]])
        crop_size[slicing_axis] = img_3d_rot[idx].shape[slicing_axis]
        if slicing_axis == 0:
            img_3d_out[s, ...] = crop_center_3d(img_3d_rot[idx], crop_size)
        elif slicing_axis == 1:
            img_3d_out[:, s, :] = crop_center_3d(img_3d_rot[idx], crop_size)
        else:
            img_3d_out[..., s] = crop_center_3d(img_3d_rot[idx], crop_size)
    log.info("Saving BlockTime --- %s seconds ---" % (time.time() - block_time))
    return img_3d_out


@jit(nopython=True, parallel=True)
def remove_labels(cc3d_area_removing, labels_out, area_th=36):
    cc_size = np.bincount(labels_out.flat)[1:]
    area_counter = 0
    for idx in prange(len(cc_size)):
        if cc_size[idx] < area_th:
            area_counter += 1
            # print(f"active {l} - removing label: {idx}")
            for x in prange(cc3d_area_removing.shape[0]):
                for y in prange(cc3d_area_removing.shape[1]):
                    for z in prange(cc3d_area_removing.shape[2]):
                        if labels_out[x, y, z] == (idx + 1):
                            cc3d_area_removing[x, y, z] = 0

    # cc3d_area_removing *= 0
    return cc3d_area_removing, area_counter


def do_post_processing(logits_3d_all):
    tmp = np.zeros(logits_3d_all.shape, dtype=np.uint8)
    tmp[(logits_3d_all == 2)] = 2
    tmp[(logits_3d_all == 3)] = 3
    tmp = closing(opening(tmp, ball(1)), ball(1))
    logits_3d_all[(logits_3d_all == 2) | (logits_3d_all == 3)] = 0
    logits_3d_all[(tmp == 2) | (tmp == 3)] = tmp[(tmp == 2) | (tmp == 3)]

    # cc removing
    labels = [1, 2, 3]
    for l in labels:
        log.info(f"Removing CC3d for label: {l}")
        tmp = np.zeros(logits_3d_all.shape)
        tmp[logits_3d_all == l] = 1
        labels_out, N = cc3d.connected_components(tmp.astype(np.uint8), return_N=True)
        logits_3d_all, area_counter = remove_labels(logits_3d_all, labels_out)
        log.info(f"Removed {area_counter} areas for label {l}")
    return logits_3d_all
