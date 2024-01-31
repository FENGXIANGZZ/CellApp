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

def stack_nuc_slices(para):
    [origin_files, save_folder, embryo_name, tp, out_size, num_slice, res] = para

    out_stack = []
    save_file_name = "{}_{}_rawNuc.nii.gz".format(embryo_name, str(tp).zfill(3))
    for idx in range((tp - 1) * num_slice, tp * num_slice):
        raw_file_name = origin_files[idx]
        img = np.asanyarray(Image.open(raw_file_name))
        out_stack.insert(0, img)
    img_stack = np.transpose(np.stack(out_stack), axes=(1, 2, 0))
    img_stack = resize(image=img_stack, output_shape=out_size, preserve_range=True, order=1).astype(np.uint8)
    nib_stack = nib.Nifti1Image(img_stack, np.eye(4))
    nib_stack.header.set_xyzt_units(xyz=3, t=8)
    nib_stack.header["pixdim"] = [1.0, res[0], res[1], res[2], 0., 0., 0., 0.]
    nib.save(nib_stack, os.path.join(save_folder, save_file_name))