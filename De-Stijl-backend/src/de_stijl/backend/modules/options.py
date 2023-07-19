import argparse
import os


class Options():
    def __init__(self):
        self.initialized = False
    
    def initialize(self, parser):
        # extractor configurations
        parser.add_argument('--ncolors', type=str, default='middle', help='less|middle|more')
        parser.add_argument('--slic_compactness', type=int, default=20, help='>=20')
        parser.add_argument('--color_type', type=str, default='average', help='average|dominant')
        # recolorizer configurations
        parser.add_argument('--hint_sparsity', type=float, default=20, help='hint sparsity from 0 to 1')
        # extra configurations
        parser.add_argument('--ckpt_dir', type=str, default='/home/xinyu_shi/Documents/de-stijl/De-Stijl-backend/checkpoints', help='checkpoint_path')
        # change to your path
        self.initialized = True
        return parser

    def gather_options(self):
        if not self.initialized:  # check if it has been initialized
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser)
        # get the basic options
        opt, _ = parser.parse_known_args()
        self.parser = parser
        return parser.parse_args()

    def print_options(self, opt):
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)

    def parse(self):
        opt = self.gather_options()
        self.print_options(opt)
        self.opt = opt
        return self.opt
