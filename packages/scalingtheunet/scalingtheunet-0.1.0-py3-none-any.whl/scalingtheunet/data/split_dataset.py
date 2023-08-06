import argparse
import logging
import os
import re
from pathlib import Path

import numpy as np
import ray
from dicereg.utils.file_system import recursive_walk
from dotenv import find_dotenv, load_dotenv
from icecream import ic
from natsort import natsorted
from sklearn.model_selection import RepeatedKFold

# from scalingtheunet.utils.file_system import load_d2_to_d3, recursive_walk

log = logging.getLogger(__name__)

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())


def create_splitting_file(idx_list, data_root, list_folders_dataset, cv, r, phase, data_name):
    x = []
    y = []
    for idx in idx_list:
        folder = list_folders_dataset[idx]
        for file_path in recursive_walk(os.path.join(data_root, folder, "images")):
            x.append(file_path)
            y.append(file_path.replace("images/", "masks/"))

    x = natsorted(x)
    y = natsorted(y)

    with open(f'{os.environ["PROJECT_DIR"]}/data/{data_name}_data_{phase}_cv{cv}_rep{r}.txt', "w") as fp:
        for p_img, p_mask in zip(x, y):
            ary_img = p_img.split("/")
            ary_mask = p_mask.split("/")
            ary_img = ("HZG_screw_implant/processed/{data_name}_2d_ClipNorm/" + ary_img[-3], ary_img[-1])
            ary_mask = ("HZG_screw_implant/processed/{data_name}_2d_ClipNorm/" + ary_mask[-3], ary_mask[-1])
            if ary_img == ary_mask:
                fp.write("%s %s\n" % tuple(ary_img))
            else:
                print("Skipping ", ary_img)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datatype", type=str, default="TiPEEK", help="datatype name")
    return parser.parse_args()


# get all folder in a directory and use pathlib
def get_list_folders_pathlib(data_root):
    list_folders = []
    for file_path in Path(data_root).iterdir():
        if file_path.is_dir():
            list_folders.append(file_path.name)
    return np.array(list_folders)


if __name__ == "__main__":
    args = parse_args()
    datatype = args.datatype

    list_folders = get_list_folders_pathlib(
        f"{os.environ['PROJECT_DIR']}/data/HZG_screw_implant/processed/{datatype}_2d_ClipNorm"
    )

    data_root = f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/processed/{datatype}_2d_ClipNorm/'
    random_state = 12883823
    num_splits = 4
    n_repeats = 1

    rkf = RepeatedKFold(n_splits=num_splits, n_repeats=n_repeats, random_state=random_state)
    for r, (train, test) in enumerate(rkf.split(list_folders)):
        cv = r % num_splits
        r = r // num_splits
        print(list_folders[train])
        print(list_folders[test])
        create_splitting_file(train, data_root, list_folders, cv, r, phase="train", data_name=datatype)
        create_splitting_file(test, data_root, list_folders, cv, r, phase="val", data_name=datatype)
        break
