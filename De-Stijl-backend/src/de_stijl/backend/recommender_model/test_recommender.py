"""General-purpose test script for image-to-image translation.

Once you have trained your model with train.py, you can use this script to test the model.
It will load a saved model from '--checkpoints_dir' and save the results to '--results_dir'.

It first creates model and dataset given the option. It will hard-code some parameters.
It then runs inference for '--num_test' images and save results to an HTML file.

Example (You need to train models first or download pre-trained models from our website):
    Test a CycleGAN model (both sides):
        python test.py --dataroot ./datasets/maps --name maps_cyclegan --model cycle_gan

    Test a CycleGAN model (one side only):
        python test.py --dataroot datasets/horse2zebra/testA --name horse2zebra_pretrained --model test --no_dropout

    The option '--model test' is used for generating CycleGAN results only for one side.
    This option will automatically set '--dataset_mode single', which only loads the images from one set.
    On the contrary, using '--model cycle_gan' requires loading and generating results in both directions,
    which is sometimes unnecessary. The results will be saved at ./results/.
    Use '--results_dir <directory_path_to_save_result>' to specify the results directory.

    Test a pix2pix model:
        python test.py --dataroot ./datasets/facades --name facades_pix2pix --model pix2pix --direction BtoA

See options/base_options.py and options/test_options.py for more test options.
See training and test tips at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md
See frequently asked questions at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/qa.md
"""
import torchvision.transforms as transforms
import torch
from .options.test_options import TestOptions
from .models import create_model
from .util import util

def load_recommender_model(ckpt_dir, ckpt_type):
    opt = TestOptions().parse()  
    opt.num_threads = 0   
    opt.batch_size = 1    
    opt.serial_batches = True  
    opt.no_flip = True    
    opt.display_id = -1   

    model = create_model(opt)      
    model.setup(opt, ckpt_dir=ckpt_dir, ckpt_type=ckpt_type)  
    model.eval()             
    return model

def recommender_test(input, model):
    opt = TestOptions().parse() 
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    key_name = ['A', 'B', 'C']
    for key in input.keys():
        if key in key_name:
            input[key] = transform(input[key])
            # input[key] = input[key].cuda()
            input[key] = torch.unsqueeze(input[key], 0)
    model.set_input(input)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()  # get image results
    out_image = util.tensor2im(visuals['fake'])
    return out_image

