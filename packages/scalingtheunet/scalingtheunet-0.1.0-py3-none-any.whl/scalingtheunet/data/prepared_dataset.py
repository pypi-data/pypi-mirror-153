import argparse
import os
from pathlib import Path

import dotenv
import numpy as np
from mpire import WorkerPool

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)


def slice_and_save_img(shared_data, axis, idx, data_dir):
    img, mask = shared_data
    if axis == 0:
        img_out = img[idx, :, :]
        mask_out = mask[idx, :, :]
    elif axis == 1:
        img_out = img[:, idx, :]
        mask_out = mask[:, idx, :]
    else:
        img_out = img[:, :, idx]
        mask_out = mask[:, :, idx]

    np.save(f"{data_dir}/images/slice{idx:04}_projection{axis}_pre.npy", img_out)
    np.save(f"{data_dir}/masks/slice{idx:04}_projection{axis}_pre.npy", mask_out)


def do_processing(folder, fix_data_problem=False):
    global datatype
    data_path = Path(f"{os.environ['PROJECT_DIR']}/data/HZG_screw_implant/raw")
    # Do some image processing.

    img = np.load(data_path / folder / "image" / "volume_3d.npy")
    mask = np.load(data_path / folder / "mask" / "mask_3d.npy").astype(np.uint8)
    unique_values = np.unique(mask)
    for i in range(len(unique_values)):
        mask[mask == unique_values[i]] = i

    img_shape = img.shape
    if fix_data_problem:
        p_low = np.percentile(img[img > 0], 0.5)
        p_high = np.percentile(img[img > 0], 99.9)
    else:
        p_low = np.percentile(img, 0.5)
        p_high = np.percentile(img, 99.9)
    img = np.clip(img, p_low, p_high)
    # norm float data to [0, 1]
    img = (img - np.min(img)) / (np.max(img) - np.min(img))

    # convert from 3D to 2D slices (each direction)
    data_dir = f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/processed/{datatype}_2d_ClipNorm/{folder}'
    if not os.path.isdir(f"{data_dir}/images"):
        os.makedirs(f"{data_dir}/images/")
        os.makedirs(f"{data_dir}/masks/")

    processing_list = []
    for axis in range(3):
        for idx in range(img_shape[axis]):
            processing_list.append((axis, idx, data_dir))

    # if -1, num_workers set to total cpu count
    num_wokers = -1
    if num_wokers == -1:
        num_cpus = os.cpu_count()

    if num_cpus > len(processing_list):
        num_cpus = len(processing_list)

    with WorkerPool(n_jobs=num_cpus // 4, shared_objects=(img, mask)) as pool:
        results = pool.map(slice_and_save_img, processing_list, progress_bar=False)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datatype", type=str, default="TiPEEK", help="datatype name")
    return parser.parse_args()


if __name__ == "__main__":
    global datatype
    # parese command line argument datatype
    args = parse_args()
    processing_list = []
    if args.datatype == "TiPEEK":
        list_folders = ["113666_PEEK", "113668_PEEK", "113680_PEEK"]
        # list_folders = ["113666_PEEK"]
        processing_list += [{"folder": f, "fix_data_problem": True} for f in list_folders]
        list_folders = ["113736_PEEK", "113740_PEEK", "113741_PEEK", "113815_Ti", "113816_Ti", "113819_Ti"]
    elif args.datatype == "Mg":
        list_folders = [
            "113724_Mg10",
            "113726_Mg5",
            "113728_Mg10",
            "113731_Mg10",
            "syn018_Mg10Gd",
            "syn020_Mg10Gd",
            "syn021_Mg10Gd",
            "syn022_Mg5Gd",
            "syn026_Mg10Gd",
            "syn030_Mg10Gd",
            "syn032_Mg10Gd",
            "syn033_Mg10Gd",
            "syn038_Mg10Gd",
            "syn041_Mg5Gd",
            "syn009_Mg5Gd",
            "113734_Mg5",
            "113729_Mg5",
        ]
    datatype = args.datatype
    processing_list += [{"folder": f, "fix_data_problem": False} for f in list_folders]
    with WorkerPool(n_jobs=4, daemon=False) as pool:
        # This will work just fine
        pool.map(do_processing, processing_list, iterable_len=len(processing_list), progress_bar=True)
