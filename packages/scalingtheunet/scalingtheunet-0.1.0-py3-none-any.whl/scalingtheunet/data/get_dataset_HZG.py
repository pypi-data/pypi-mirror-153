import os
import re
from pathlib import Path

import dotenv
import numpy as np
from icecream import ic
from mpire import WorkerPool

from scalingtheunet.utils.file_system import load_d2_to_d3

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)


def link_data_syn(root_dir, data_folder, create_new=True):
    for img_folder, mask_folder in data_folder:
        experiment_name = img_folder.split("/")[0]
        experiment_name = experiment_name.split("_")
        number = int(re.findall(r"\d+", experiment_name[0])[0])
        dst_folder = Path(f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/external/syn{number:03}_{experiment_name[2]}')
        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)
            print(f"Creating sym links for:\n\t {dst_folder}")
            os.symlink(root_dir / Path(img_folder), dst_folder / "image")
            os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")
        else:
            print(f"Found sym links for:\n\t {dst_folder}")
            if create_new:
                print(f"Creating new sym links")
                os.unlink(dst_folder / "image")
                os.symlink(root_dir / Path(img_folder), dst_folder / "image")
                os.unlink(dst_folder / "mask")
                os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")


def link_data_p05(root_dir, data_folder, create_new=True):
    for material, img_folder, mask_folder in data_folder:
        experiment_name = img_folder.split("/")[0]
        if experiment_name == "..":
            experiment_name = img_folder.split("/")[1]

        dst_folder = Path(f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/external/{experiment_name}_{material}')
        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)

            print(f"Creating sym links for:\n\t {dst_folder}")
            os.symlink(root_dir / Path(img_folder), dst_folder / "image")
            os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")
        else:
            print(f"Found sym links for:\n\t {dst_folder}")
            if create_new:
                print(f"Creating new sym links")
                os.unlink(dst_folder / "image")
                os.symlink(root_dir / Path(img_folder), dst_folder / "image")
                os.unlink(dst_folder / "mask")
                os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")


def link_data_hq(data_folder, create_new=True):
    for root_dir, material, img_folder, mask_folder, mask_HQ_folder in data_folder:
        experiment_name = img_folder.split("/")[0]
        if len(experiment_name.split("_")) > 1:
            experiment_name = experiment_name.split("_")
            number = int(re.findall(r"\d+", experiment_name[0])[0])
            dst_folder = Path(f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/external/syn{number:03}_{material}')
        else:
            dst_folder = Path(f'{os.environ["PROJECT_DIR"]}/data/HZG_screw_implant/external/{experiment_name}_{material}')

        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)

            print(f"Creating sym links for:\n\t {dst_folder}")
            os.symlink(root_dir / Path(img_folder), dst_folder / "image")
            os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")
            os.symlink(root_dir / Path(mask_HQ_folder), dst_folder / "mask_HQ")
        else:
            print(f"Found sym links for:\n\t {dst_folder}")
            if create_new:
                print(f"Creating new sym links")
                os.unlink(dst_folder / "image")
                os.symlink(root_dir / Path(img_folder), dst_folder / "image")
                os.unlink(dst_folder / "mask")
                os.symlink(root_dir / Path(mask_folder), dst_folder / "mask")
                os.unlink(dst_folder / "mask_HQ")
                os.symlink(root_dir / Path(mask_HQ_folder), dst_folder / "mask_HQ")


def create_raw_data(folder):
    data_folders = [f.path for f in os.scandir(folder) if f.is_dir()]
    for data_folder in data_folders:
        data_vol = load_d2_to_d3(data_folder)
        dst_folder = data_folder.replace("external", "raw")
        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)
        if "mask" in dst_folder:
            np.save(f"{dst_folder}/mask_3d.npy", data_vol)
        else:
            np.save(f"{dst_folder}/volume_3d.npy", data_vol)


if __name__ == "__main__":
    """
    link external data to project dir for Syn
    """
    root_dir = Path("/asap3/petra3/gpfs/p05/2017/data/11003440/processed")
    data_folder = [
        (
            "syn18_88L_Mg10Gd_4w/segmentation/2017_11003440_syn18_88L_Mg10Gd_4w_reco",
            "syn18_88L_Mg10Gd_4w/segmentation/2017_11003440_syn18_88L_Mg10Gd_4w_labels",
        ),
        (
            "syn20_62R_Mg10Gd_12w/segmentation/2017_11003440_syn20_62R_Mg10Gd_12w_original",
            "syn20_62R_Mg10Gd_12w/segmentation/2017_11003440_syn20_62R_Mg10Gd_12w_labels",
        ),
        (
            "syn21_82R_Mg10Gd_8w/segmentation/2017_11003440_syn21_82R_Mg10Gd_8w_reco",
            "syn21_82R_Mg10Gd_8w/segmentation/2017_11003440_syn21_82R_Mg10Gd_8w_labels",
        ),
        (
            "syn22_62L_Mg5Gd_12w/segmentation/2017_11003440_syn22_62L_Mg5Gd_12w_reco",
            "syn22_62L_Mg5Gd_12w/segmentation/2017_11003440_syn22_62L_Mg5Gd_12w_labels",
        ),
        (
            "syn26_69R_Mg10Gd_12w/segmentation/2017_11003440_syn26_69R_Mg10Gd_12w_reco",
            "syn26_69R_Mg10Gd_12w/segmentation/2017_11003440_syn26_69R_Mg10Gd_12w_labels",
        ),
        (
            "syn29_78L_Mg5Gd_8w/diana/workflow/final/toforward/syn29_rr_original_60-780__130-715",
            "syn29_78L_Mg5Gd_8w/diana/workflow/final/toforward/syn29_rr_60-780__130-715",
        ),
        (
            "syn30_87L_Mg10Gd_4w/segmentation/2017_11003440_syn30_87L_Mg10Gd_4w_reco",
            "syn30_87L_Mg10Gd_4w/segmentation/2017_11003440_syn30_87L_Mg10Gd_4w_labels",
        ),
        (
            "syn32_99R_Mg10Gd_4w/segmentation/2017_11003440_syn32_99R_Mg10Gd_4w_reco",
            "syn32_99R_Mg10Gd_4w/segmentation/2017_11003440_syn32_99R_Mg10Gd_4w_labels",
        ),
        (
            "syn33_80R_Mg10Gd_8w/segmentation/2017_11003440_syn33_80R_Mg10Gd_8w_reco_32bit",
            "syn33_80R_Mg10Gd_8w/segmentation/2017_11003440_syn33_80R_Mg10Gd_8w_labels",
        ),
        (
            "syn38_73R_Mg10Gd_8w/segmentation/2017_11003440_syn38_73R_Mg10Gd_8w_reco",
            "syn38_73R_Mg10Gd_8w/segmentation/2017_11003440_syn38_73R_Mg10Gd_8w_labels",
        ),
        (
            "syn41_63L_Mg5Gd_12w/segmentation/2017_11003440_syn41_63L_Mg5Gd_12w_reco",
            "syn41_63L_Mg5Gd_12w/segmentation/2017_11003440_syn41_63L_Mg5Gd_12w_labels",
        ),
        (
            "syn46_88R_Mg5Gd_4w/diana/workflow/final/toforward/syn46_rr_original_1-700__10-685",
            "syn46_88R_Mg5Gd_4w/diana/workflow/final/toforward/syn46_rr_1-700__10-685",
        ),
        (
            "syn47_100AL_Mg5Gd_4w/diana/workflow/final/toforward/syn47_rr_original_1-806__10-625",
            "syn47_100AL_Mg5Gd_4w/diana/workflow/final/toforward/syn47_rr_1-806__10-625",
        ),
        (
            "syn49_80L_Mg5Gd_8w/diana/workflow/final/toforward/syn49_rr_original_30-760__1-610",
            "syn49_80L_Mg5Gd_8w/diana/workflow/final/toforward/syn49_rr_30-760__1-610",
        ),
        (
            "syn51_87R_Mg5Gd_4w/diana/workflow/final/toforward/syn51_rr_original_35-780__20-610",
            "syn51_87R_Mg5Gd_4w/diana/workflow/final/toforward/syn51_rr_35-780__20-610",
        ),
    ]

    link_data_syn(root_dir, data_folder, create_new=True)

    """
    link external data to project dir for P05
    """
    root_dir = "/asap3/petra3/gpfs/external/2019/data/50000258/processed/resampled"
    data_folder = [
        ("Mg10", "113724/113724_Philipp_original/113724_original_tiff", "113724/113724_Philipp_segmented_workflow"),
        ("Mg5", "113726/113726_Philipp_original/113726_original_tiff", "113726/113726_Philipp_segmented_workflow"),
        ("Mg10", "113728/113728_Philipp_original/113728_original_tiff", "113728/113728_Philipp_segmented_workflow"),
        ("Mg10", "113731/113731_Philipp_original/113731_original_tiff", "113731/113731_Philipp_segmented_corrected"),
        # peek
        (
            "PEEK",
            "113736/113736_Philipp_oryginal/113736_oryginal_tiff",
            "113736/113736_Philipp_segmented/113736_segmented_tiff",
        ),
        (
            "PEEK",
            "113740/113740_Philipp_oryginal/113740_oryginal_tiff",
            "113740/113740_Philipp_segmented/113740_segmented_tiff",
        ),
        (
            "PEEK",
            "113741/113741_Philipp_oryginal/113741_oryginal_tiff",
            "113741/113741_Philipp_segmented/113741_segmented_tiff",
        ),
        ("PEEK", "../113666/original_resampled", "../113666/1136666_segmented"),
        ("PEEK", "../113668/original_resampled", "../113668/113668_segmented"),
        ("PEEK", "../113680/original_resampled", "../113680/113680_segmented"),
        # TI
        (
            "Ti",
            "113815/113815_Philipp_oryginal/113815_oryginal_tiff",
            "113815/113815_Philipp_segmented/113815_segmented_tiff",
        ),
        (
            "Ti",
            "113816/113816_Philipp_oryginal/113816_oryginal_tiff",
            "113816/113816_Philipp_segmented/113816_segmented_tiff",
        ),
        (
            "Ti",
            "113819/113819_philipp_oryginal/113819_oryginal_tiff",
            "113819/113819_Philipp_segmented/113819_segmented_tiff",
        ),
    ]
    link_data_p05(root_dir, data_folder, create_new=True)

    """
    link external data to project dir for HQ
    """
    # HQ data = syn009, 113729Mg5, 113734Mg5
    data_folder = [
        (
            "/asap3/petra3/gpfs/p05/2018/data/11004263/processed",
            "Mg5Gd",
            "syn009_64L_Mg5Gd_12w_a/Philipp_oryginal",
            "syn009_64L_Mg5Gd_12w_a/reco_a+b/segmented",
            "syn009_64L_Mg5Gd_12w_a/Philipp_segmented",
        ),
        (
            "/asap3/petra3/gpfs/external/2019/data/50000258/processed/resampled",
            "Mg5",
            "113729/113729_Philipp_original_corrected/113729_original_tiff",
            "113729/113729_Philipp_segmented_workflow/113729_segmentation_workflow_tiff",
            "113729/113729_segmented_hq/segmented_hq",
        ),
        (
            "/asap3/petra3/gpfs/external/2019/data/50000258/processed/resampled",
            "Mg5",
            "113734/Philipp/Philipp",
            "113734/113734_Philipp_segmented_workflow",
            "113734/113734_segmented_hq/segmented_hq",
        ),
    ]

    link_data_hq(data_folder, create_new=True)

    # create raw data for preproceesing
    # get all folders in a directory with pathlib
    external_dir = Path(os.environ["PROJECT_DIR"]) / "data" / "HZG_screw_implant" / "external"
    external_data_folders = [f.path for f in os.scandir(external_dir) if f.is_dir()]
    if not os.path.isdir(str(external_dir).replace("external", "raw")):
        os.makedirs(str(external_dir).replace("external", "raw"))
    with WorkerPool(n_jobs=6) as pool:
        # This will work just fine
        pool.map(create_raw_data, external_data_folders, iterable_len=len(external_data_folders), progress_bar=True)
