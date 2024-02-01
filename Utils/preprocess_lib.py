import os
import glob
import warnings
import shutil

warnings.filterwarnings("ignore")
import numpy as np
from PIL import Image
import nibabel as nib
import pandas as pd
from tqdm import tqdm
import multiprocessing as mp
from skimage.transform import resize


def stack_nuc_slices2(para):
    [origin_files, save_folder, embryo_name, tp, out_size, num_slice, res] = para

    first_img_idx = (tp - 1) * num_slice
    bottom_img = np.asanyarray(Image.open(origin_files[first_img_idx]))
    bottom_img = np.expand_dims(bottom_img, axis=0)
    save_file_name = "{}_{}_rawNuc.nii.gz".format(embryo_name, str(tp).zfill(3))

    for idx in range(first_img_idx + 1, tp * num_slice):
        raw_file_name = origin_files[idx]
        img = np.asanyarray(Image.open(raw_file_name))
        img = np.expand_dims(img, axis=0)
        bottom_img = np.concatenate((img, bottom_img), axis=0)

    img_stack = np.transpose(bottom_img, axes=(1, 2, 0))
    return img_stack

def stack_nuc_slices(para):
    """
    作用是将每个时间点的所有阶段的照片堆叠在一起,形成一个三维立体的图片
    :param para:
    :return:
    """
    [origin_files, save_folder, embryo_name, tp, out_size, num_slice, res] = para

    out_stack = []
    save_file_name = "{}_{}_rawNuc.nii.gz".format(embryo_name, str(tp).zfill(3))
    for idx in range((tp - 1) * num_slice, tp * num_slice):
        raw_file_name = origin_files[idx]
        img = np.asanyarray(Image.open(raw_file_name))
        out_stack.insert(0, img)

    img_stack = np.transpose(np.stack(out_stack), axes=(1, 2, 0))
    img_stack = resize(image=img_stack, output_shape=out_size, preserve_range=True, order=1).astype(np.uint16)
    nib_stack = nib.Nifti1Image(img_stack, np.eye(4))
    # nib_stack.header.set_xyzt_units(xyz=3, t=8)
    # nib_stack.header["pixdim"] = [1.0, res[0], res[1], res[2], 0., 0., 0., 0.]
    nib.save(nib_stack, os.path.join(save_folder, save_file_name))

def stack_memb_slices(para):
    [origin_files, save_folder, embryo_name, tp, out_size, num_slice, res] = para

    out_stack = []
    save_file_name = "{}_{}_rawMemb.nii.gz".format(embryo_name, str(tp).zfill(3))
    for idx in range((tp-1)*num_slice, tp*num_slice):
        raw_file_name = origin_files[idx]

        img = np.asanyarray(Image.open(raw_file_name))
        out_stack.insert(0, img)
    img_stack = np.transpose(np.stack(out_stack), axes=(1, 2, 0))
    img_stack = resize(image=img_stack, output_shape=out_size, preserve_range=True, order=1).astype(np.uint8)
    nib_stack = nib.Nifti1Image(img_stack, np.eye(4))
    # nib_stack.header.set_xyzt_units(xyz=3, t=8)
    # nib_stack.header["pixdim"] = [1.0, res[0], res[1], res[2], 0., 0., 0., 0.]
    nib.save(nib_stack, os.path.join(save_folder, save_file_name))

if __name__ == '__main__':
    # origin_files =  glob.glob(os.path.join("C:\CellAltas\MembRaw\MembRaw", "181210plc1p1", "tif", "*.tif"))
    origin_files2 = glob.glob(os.path.join("C:\CellAltas\MembRaw\MembRaw", "181210plc1p1", "tifR", "*.tif"))
    raw_file_name = origin_files2[1359]
    # list1 = []
    # list2 = []
    # for f in origin_files:
    #     list1.append(f[-28:])
    #
    # for f in origin_files2:
    #     list2.append(f[-28:])
    #
    # for f in list1:
    #     if f not in list2:
    #         print(f)
    #
    # print(len(list1))
    # print(len(list2))



