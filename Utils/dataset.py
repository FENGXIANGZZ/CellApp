import glob
import os
import numpy as np
import torch
from torch.utils.data import Dataset
import pickle
import nibabel as nib

paths = glob.glob(os.path.join("E:\work", "RawStack", "181210plc1p1", "RawMemb", "*.nii.gz"))
print(paths)
embryos_name_tp = ['_'.join(os.path.basename(path).split(".")[0].split('_')[:2]) for path in paths]
print(embryos_name_tp)


class MembsegDataset(Dataset):

    def __init__(self, root, embryoname, suffix="*.nii.gz"):

        self.project_path = root
        self.rawmemb_paths = glob.glob(os.path.join(root, "RawStack", embryoname, "RawMemb", suffix))
        self.rawnuc_paths = glob.glob(os.path.join(root, "RawStack", embryoname, "RawNuc", suffix))

        self.embryos_name_tp = ['_'.join(os.path.basename(path).split(".")[0].split('_')[:2]) for path in self.rawmemb_paths]


    def __getitem__(self, item):

        embryo_name_tp = self.embryos_name_tp[item]

        raw_shape = loaded_dict['raw_memb'].shape
        raw_memb = self.transforms([loaded_dict["raw_memb"]], embryo_name_tp)
        # print(self.transforms)
        # print(raw_mem,seg_mem)
        raw_memb = self.volume2tensor([raw_memb], dim_order=[2, 0, 1])
        return raw_memb, raw_shape, middle_path_name

    def volume2tensor(self, volumes0, add_channel=True, dim_order=None):

        '''
        :param volumes0: raw_memb, seg_memb, raw_nuc, seg_nuc
        :param dim_order:
        :return:
        '''
        volumes = volumes0 if isinstance(volumes0, list) else [volumes0]
        outputs = []
        for volume in volumes:
            # add one axis, 3D=>4D add channel
            if add_channel:
                volume = volume.transpose(dim_order)[np.newaxis, ...]  # add a batch size dimension here
            else:
                volume = volume.transpose(dim_order)
            # print(volume.shape)
            volume = np.ascontiguousarray(volume)  #
            # print(volume.shape)
            volume = torch.from_numpy(volume)
            outputs.append(volume)

        return outputs if isinstance(volumes0, list) else outputs[0]

    def __len__(self):
        return len(self.embryos_name_tp)

    def __str__(self):
        return 'Validating data'

