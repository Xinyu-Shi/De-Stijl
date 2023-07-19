import os
from de_stijl.backend.recommender_model.data.base_dataset import BaseDataset, get_params, get_transform
from de_stijl.backend.recommender_model.data.image_folder import make_dataset
from PIL import Image
from skimage import color 
import numpy as np
import torchvision.transforms as transforms
import torch

class AlignedDataset(BaseDataset):
    """A dataset class for paired image dataset.

    It assumes that the directory '/path/to/data/train' contains image pairs in the form of {A,B}.
    During test time, you need to prepare a directory '/path/to/data/test'.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)  # get the image directory
        self.AB_paths = sorted(make_dataset(self.dir_AB, opt.max_dataset_size))  # get image paths
        assert(self.opt.load_size >= self.opt.crop_size)   # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor) - - an image in the input domain
            B (tensor) - - its corresponding image in the target domain
            A_paths (str) - - image paths
            B_paths (str) - - image paths (same as A_paths)
        """
        # read a image given a random integer index
        AB_path = self.AB_paths[index]
        AB = Image.open(AB_path).convert('RGB')
        w, h = AB.size
        w0 = int(w / 5)
        inputs = {
            'input': AB.crop((0, 0, w0, h)),
            'theme': AB.crop((w0, 0, w0*2, h)),
            'bg': AB.crop((w0*2, 0, w0*3, h)),
            'canvas': AB.crop((w0*3, 0, w0*4, h)),
            'GT': AB.crop((w0*4, 0, w0*5, h)),
        }

        # apply the same transform to both A and B
        transform_params = get_params(self.opt, inputs['input'].size)
        input_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1), convert=False)
        for key in inputs.keys():
            inputs[key] = input_transform(inputs[key])
            inputs[key] = np.array(inputs[key])
            inputs[key] = color.rgb2lab(inputs[key]/255.).astype(np.float32)
            inputs[key] = transforms.ToTensor()(inputs[key])
            inputs[key][[0], ...] = inputs[key][[0], ...] / 50.0 - 1.0
            inputs[key][[1, 2], ...] = inputs[key][[1, 2], ...] / 110.0
        condition = torch.cat([inputs['theme'], inputs['bg'], inputs['canvas']], 0) 

        return {'A': inputs['input'], 'B': inputs['GT'], 'C': condition, 'A_paths': AB_path, 'B_paths': AB_path}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.AB_paths)
