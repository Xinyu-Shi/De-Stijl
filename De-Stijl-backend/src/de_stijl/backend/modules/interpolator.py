import torch
from collections import OrderedDict
import os

class Interpolator():
    def __init__(self, opt):
        self.ckpt_dir = opt.ckpt_dir
        self.alpha = [0.2, 0.4, 0.6, 0.8]
        self.path_A = os.path.join(self.ckpt_dir, 'image_10_net_G.pth')
        self.path_B = os.path.join(self.ckpt_dir, 'image_rec_net_G.pth')
        
    
    def interpolate(self):
        net_A = torch.load(self.path_A)
        net_B = torch.load(self.path_B)
        for alpha in self.alpha:
            target_path = os.path.join(self.ckpt_dir, f'image_{int(alpha * 10)}_net_G.pth')
            net_interp = OrderedDict()
            for k, v_A in net_A.items():
                v_B = net_B[k]
                net_interp[k] = alpha * v_A + (1 - alpha) * v_B
            torch.save(net_interp, target_path)

if __name__ == '__main__':
    from de_stijl.backend.modules.options import Options
    opt = Options().parse()
    interpolator = Interpolator(opt)
    interpolator.interpolate()