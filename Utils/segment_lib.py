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
import traceback
import torch


def segmentation(configs):

    try:
        with torch.no_grad():
            [data, model, device, save_path] = configs
            model.eval()
            raw_memb = data[0]
            raw_memb_shape = data[1]
            embryo_name_tp = data[2][0]
            raw_memb_shape = (raw_memb_shape[0].item(), raw_memb_shape[1].item(), raw_memb_shape[2].item())
            pred_memb = model(raw_memb.to(device))
            pred_memb = pred_memb[0] if len(pred_memb) > 1 else pred_memb

            pred_memb = pred_memb[0, 0, :, :, :]
            pred_memb = pred_memb.cpu().numpy().transpose([1, 2, 0])
            pred_memb = resize(pred_memb,
                               raw_memb_shape,
                               mode='constant',
                               cval=0,
                               order=1,
                               anti_aliasing=True)

            save_name = os.path.join(save_path, embryo_name_tp + "_segMemb.nii.gz")
            nib_stack = nib.Nifti1Image((pred_memb * 256).astype(np.int16), np.eye(4))
            nib.save(nib_stack, save_name)

    except Exception as e:
        return "Threadpool return exception: {}".format(e)

