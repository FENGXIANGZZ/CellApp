import glob
import os
import numpy as np
import torch
from torch.utils.data import Dataset
import pickle
import nibabel as nib
from skimage.transform import resize


class MembsegDataset(Dataset):

    def __init__(self, root, embryoname, is_input_nuc, transforms=None, suffix="*.nii.gz"):

        self.project_path = root
        self.rawmemb_paths = glob.glob(os.path.join(root, "RawStack", embryoname, "RawMemb", suffix))
        self.embryos_name_tp = ['_'.join(os.path.basename(path).split(".")[0].split('_')[:2]) for path in self.rawmemb_paths]
        assert len(self.embryos_name_tp) > 0
        self.embryoname = embryoname
        self.isNuc = is_input_nuc
        self.suffix = suffix
        self.transforms = eval(transforms or "Identity()")


    def __getitem__(self, item):
        embryo_name_tp = self.embryos_name_tp[item]

        if self.isNuc:
            rawnuc_paths = glob.glob(os.path.join(self.project_path, "RawStack", self.embryoname, "RawNuc", self.suffix))
            assert len(self.rawmemb_paths) == len(rawnuc_paths)

            raw_memb_path = self.rawmemb_paths[item]
            raw_nuc_path = os.path.join(self.project_path, "RawStack", self.embryoname, "RawNuc", "{}_rawNuc.nii.gz".format(embryo_name_tp))

            raw_memb = nib.load(raw_memb_path).get_fdata()
            raw_nuc = nib.load(raw_nuc_path).get_fdata()

        else:
            raw_memb = nib.load(self.rawmemb_paths[item]).get_fdata()
            print(raw_memb, raw_memb.shape)

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



if __name__ == '__main__':
    paths = glob.glob(os.path.join("E:\work", "RawStack", "181210plc1p1", "RawMemb", "*.nii.gz"))
    data = nib.load(paths[0]).get_fdata()
    print(data, data.shape)
    img_stack = resize(image=data, output_shape=[], preserve_range=True, order=1).astype(np.uint16)

