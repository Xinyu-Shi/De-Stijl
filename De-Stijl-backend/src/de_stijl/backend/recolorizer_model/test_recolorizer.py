import torch
import torchvision.transforms as transforms
from .options.train_options import TrainOptions
from .models import create_model
from .util import util

def load_recolorizer_model(ckpt_dir):
    opt = TrainOptions().parse()
    opt.load_model = True
    opt.num_threads = 1  
    opt.batch_size = 1  
    opt.display_id = -1  # no visdom display
    opt.serial_batches = True
    opt.aspect_ratio = 1.
    
    model = create_model(opt)
    model.setup(opt, ckpt_dir=ckpt_dir)
    model.eval()
    return model

def recolorize_test(input, model, num_points=15):
    sample_p = .125
    to_visualize = ['gray', 'real', 'fake_reg', 'hint']
    opt = TrainOptions().parse()
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    input = transform(input)
    data_raw = input.cuda()
    data_raw = torch.unsqueeze(data_raw, 0)
    data = util.get_colorization_data(data_raw, opt, num_points=num_points, ab_thresh=0., p=sample_p)
    model.set_input(data)
    model.test(True)  # True means that losses will be computed
    visuals = util.get_subset_dict(model.get_current_visuals(), to_visualize)
    out_img = util.tensor2im(visuals['fake_reg'])
    return out_img

