import logging
import os
import re

import numpy as np
from natsort import natsorted
from skimage import io

log = logging.getLogger(__name__)


def recursive_walk(rootdir):
    for r, dirs, files in os.walk(rootdir):
        for f in files:
            yield os.path.join(r, f)


def get_filepaths_with_regex(root_path: str, file_regex: str):
    files_paths = []
    pattern = re.compile(file_regex)
    files = os.listdir(root_path)
    for file in files:
        if pattern.match(file):
            files_paths.append(os.path.join(root_path, file))
    return files_paths


def load_all_tif_files(root_path, search_regex="vol_\d{6}.tif"):
    tif_files = get_filepaths_with_regex(root_path, search_regex)
    if not len(tif_files) > 0:
        log.warn(f'RegEx did not find a file. Falling back to load all "*.tif" files.')
        files = os.listdir(root_path)
        tif_files = []
        for file in files:
            if ".tif" in file:
                tif_files.append(os.path.join(root_path, file))

    tif_files = natsorted(tif_files)
    return tif_files


def load_d2_to_d3(path):
    tif_files = load_all_tif_files(path)
    if not len(tif_files) > 0:
        log.warn(f'Did not find any "*.tif" file.')
        return None
    img = io.imread(tif_files[0])
    shape_xy = img.shape
    z = len(tif_files)
    img_vol = np.zeros((z,) + shape_xy, dtype=np.dtype("float32"))
    for i, f in enumerate(tif_files):
        img = io.imread(f)
        img = np.nan_to_num(img)
        img_vol[i] = img
    return img_vol
