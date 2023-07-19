import math
from skimage import io, color
import numpy as np
from tqdm import tqdm
import yaml
import os
import argparse
import imgaug.augmenters as iaa
import PIL
import json
from de_stijl.backend.modules.extractor import Extractor
from de_stijl.backend.modules.options import Options



def is_image_file(filename):
    return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])

def decode_HEXcode(hex_code):
    rgb = PIL.ImageColor.getcolor(hex_code, "RGB")
    return rgb

def generate_theme_image(hex_codes):
    img = np.zeros([1, len(hex_codes),3],dtype=np.uint8)
    for idx, hex_code in enumerate(hex_codes):
        rgb = decode_HEXcode(hex_code=hex_code)
        img[0, idx, :] = list(rgb)
    resize_aug = iaa.Resize(256, interpolation='nearest')
    img = resize_aug(image=img)
    return img

def read_theme_hex_from_json(json_path, target_dir):
    with open(json_path, 'r') as f:
        data = json.load(f)
    for image in data:
        filename = str(image['id']).zfill(4) + '.png'
        hex_codes = image['color']
        theme_img = generate_theme_image(hex_codes)
        file_path = os.path.join(target_dir, filename)
        io.imsave(file_path, theme_img)

def generate_lq_palette(palette):
    lq_aug = iaa.Sequential([
        iaa.Sometimes(0.1, iaa.Dropout2d(p=0.5)),
        iaa.SomeOf((1, 3), [
            iaa.Add((-40, 40), per_channel=0.5),
            iaa.Multiply((0.8, 1.2), per_channel=0.5),
            iaa.WithChannels([0], iaa.Add((10, 30))),
            iaa.WithChannels([1], iaa.Add((10, 30))),
            iaa.WithChannels([2], iaa.Add((10, 30))),
        ], random_order=True),
        iaa.SomeOf((0, 1), [
            iaa.Invert(0.25, per_channel=0.5),
            iaa.Solarize(0.5, threshold=(32, 128)),
        ], random_order=True),
        iaa.SomeOf((1, 3), [
            iaa.WithColorspace(to_colorspace="HSV", from_colorspace="RGB", children=iaa.WithChannels(0,iaa.Add((0, 50)))),
            iaa.WithBrightnessChannels(iaa.Add((-30, 30))),
            iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-30, 30)),
            iaa.WithHueAndSaturation(iaa.WithChannels(0, iaa.Add((0, 50)))),
            iaa.MultiplyHueAndSaturation((0.5, 1.5), per_channel=True),
            iaa.MultiplyHueAndSaturation(mul_hue=(0.5, 1.5)),
        ], random_order=True),
    ])
    lq_palette = lq_aug(image=palette)
    return lq_palette


# theme image generation
# if __name__ == '__main__':
#     json_path = '/home/xinyu/Research/AdsColorizer/ads_data/theme.json'
#     target_dir = '/home/xinyu/Research/AdsColorizer/ads_data/theme_test'
#     read_theme_hex_from_json(json_path, target_dir)

# 2D palette extraction and lq palette generation
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='extract color palette from images')
#     parser.add_argument('--dataset', default='PaletteData', type=str, help='selecting different datasets')
#     opt = parser.parse_args()
#     with open('./src/de_stijl/backend/preprocess/path.yml', 'r') as stream:
#         PATHS = yaml.load(stream)
#     target_dirs = [PATHS[opt.dataset]['target']['train'],
#                    PATHS[opt.dataset]['target']['test'],
#                    ]
#     lq_dirs = [PATHS[opt.dataset]['lq']['train'],
#                    PATHS[opt.dataset]['lq']['test'],
#                    ]
#     image_dirs = [PATHS[opt.dataset]['image']['train'],
#                   PATHS[opt.dataset]['image']['test'],
#                 ]
#     for index in range(len(target_dirs)):
#         if not os.path.exists(target_dirs[index]):
#             os.makedirs(target_dirs[index])
#         if not os.path.exists(lq_dirs[index]):
#             os.makedirs(lq_dirs[index])
    
#     opt = Options().parse()
#     palette_extractor = Extractor(opt)
#     for index, input_dir in enumerate(image_dirs):
#         print('\nComputing images from directory ' + input_dir)
#         files = [os.path.join(input_dir, x) for x in os.listdir(input_dir) if is_image_file(x)]
#         for file in tqdm(files):
#             target_path = os.path.join(target_dirs[index], os.path.basename(file))
#             lq_path = os.path.join(lq_dirs[index], os.path.basename(file))
#             image = io.imread(file)
#             palette = palette_extractor.extract(image)
#             lq_palette = generate_lq_palette(palette)
#             io.imsave(target_path, palette)
#             io.imsave(lq_path, lq_palette)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract color palette from images')
    parser.add_argument('--dataset', default='shapeData', type=str, help='selecting different datasets')

    opt = parser.parse_args()

    with open('./src/de_stijl/backend/preprocess/path.yml', 'r') as stream:
        PATHS = yaml.safe_load(stream)

    target_dirs = [PATHS[opt.dataset]['target']['train'],
                #    PATHS[opt.dataset]['palette']['test'],
                #    PATHS[opt.dataset]['palette']['valid']
                   ]
    image_dirs = [PATHS[opt.dataset]['image']['train']]
    bg_dirs = [PATHS[opt.dataset]['bg']['train']]
    theme_dirs = [PATHS[opt.dataset]['theme']['train']]
    shape_dirs = [PATHS[opt.dataset]['shape']['train']]
    gt_dirs = [PATHS[opt.dataset]['gt']['train']]

    
    for index in range(len(target_dirs)):
        if not os.path.exists(target_dirs[index]):
            os.makedirs(target_dirs[index])
    
    for index, input_dir in enumerate(image_dirs):
        print('\nComputing images from directory ' + input_dir)
        files = [os.path.join(input_dir, x) for x in os.listdir(input_dir) if is_image_file(x)]
        images = []
        for file in tqdm(files):
            bg_path = os.path.join(bg_dirs[index], os.path.basename(file))
            theme_path = os.path.join(theme_dirs[index], os.path.basename(file))
            shape_path = os.path.join(shape_dirs[index], os.path.basename(file))
            gt_path = os.path.join(gt_dirs[index], os.path.basename(file))
            target_path = os.path.join(target_dirs[index], os.path.basename(file))
            image = io.imread(file)
            bg = io.imread(bg_path)
            shape = io.imread(shape_path)
            gt = io.imread(gt_path)
            theme = io.imread(theme_path)
            output = np.hstack((image, theme, bg, theme, gt))
            io.imsave(target_path, output)
    