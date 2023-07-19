from matplotlib.pyplot import axis
import numpy as np
import PIL 
from skimage import io
from skimage import color 
from colorthief import ColorThief
import fast_colorthief
from io import BytesIO
import imgaug.augmenters as iaa
import os
from de_stijl.backend.recommender_model.test_recommender import load_recommender_model, recommender_test

class Recommender():
    def __init__(self, opt, ckpt_type='image', theme_level=10):
        self.ckpt_dir = opt.ckpt_dir
        self.ckpt_type = ckpt_type
        if self.ckpt_type == 'image': 
            self.ckpt_type = f'image_{theme_level}'
        self.model = load_recommender_model(ckpt_dir=self.ckpt_dir, ckpt_type=self.ckpt_type)

    def __construct_input(self, input, bg, theme, canvas):
        resize_aug = iaa.Resize(256, interpolation='cubic')
        self.inputs = {
            'input': input,
            'theme': theme,
            'bg': bg,
            'canvas': canvas, 
        }
        for key in self.inputs.keys():
            self.inputs[key] = resize_aug(image=self.inputs[key])
            self.inputs[key] = color.rgb2lab(self.inputs[key]/255.).astype(np.float32)
            self.inputs[key][:, :, [0]] = self.inputs[key][:, :, [0]] / 50.0 - 1.0
            self.inputs[key][:, :, [1, 2]] = self.inputs[key][:, :, [1, 2]] / 110.0
        return {'A': self.inputs['input'], 'C': np.concatenate((self.inputs['theme'], self.inputs['bg'], self.inputs['canvas']), axis=2), 'A_paths': '', 'B_paths': ''}

    def recommend(self, input, bg, theme, canvas):
        images_and_conditions = self.__construct_input(input, bg, theme, canvas)
        recommended_palette = recommender_test(images_and_conditions, self.model)
        return recommended_palette
    
    def extract_decor_color(self, decor_image):
        if np.mean(decor_image) > 253:
            if self.ckpt_type == 'shape':
                dominant_color = (255, 255, 255)
            if self.ckpt_type == 'text':
                dominant_color = (0, 0, 0)
        else:
            decor_pil = PIL.Image.fromarray(decor_image)
            decor_file = BytesIO()
            decor_pil.save(decor_file, format="PNG")
            color_palette = fast_colorthief.get_palette(decor_file, color_count=2)
            if sum(list(color_palette[0])) / 3 > 250:
                dominant_color = color_palette[1]
            else: 
                dominant_color = color_palette[0]
        return dominant_color


# test
if __name__ == '__main__':
    from de_stijl.backend.modules.options import Options
    def is_image_file(filename):
        return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])

    opt = Options().parse()
    root_path = './mockdata/templates/template05'

    image_path = f'{root_path}/results/palette_01.png'
    bg_path = f'{root_path}/bg.png'
    theme_path = f'{root_path}/theme.png'
    shape_dir = f'{root_path}/v1/shapes/'
    text_dir = f'{root_path}/v1/texts/'

    recommended_image_path = f'{root_path}/results/test_image_recommender.png'
    recommended_shape_dir = f'{root_path}/results/shapes'
    recommended_text_dir = f'{root_path}/results/texts'
    image = np.asarray(PIL.Image.open(image_path).convert('RGB'))
    bg = np.asarray(PIL.Image.open(bg_path).convert('RGB'))
    theme = np.asarray(PIL.Image.open(theme_path).convert('RGB'))
    # decor = np.asarray(PIL.Image.open(decor_path).convert('RGB'))

    image_recommender = Recommender(opt, ckpt_type='image', theme_level=2)
    shape_recommender = Recommender(opt, ckpt_type='shape')
    text_recommender = Recommender(opt, ckpt_type='text')
    recommended_palette = image_recommender.recommend(image, bg, theme, theme)
    io.imsave(recommended_image_path, recommended_palette)

    aug = iaa.Grayscale(alpha=1.0)

    shape_files = [os.path.join(shape_dir, x) for x in os.listdir(shape_dir) if is_image_file(x)]
    text_files = [os.path.join(text_dir, x) for x in os.listdir(text_dir) if is_image_file(x)]
    for shape_file in shape_files:
        shape = np.asarray(PIL.Image.open(shape_file).convert('RGB'))
        shape = np.where(shape==0, 255, shape)
        shape = aug(image=shape)
        shape_palette = shape_recommender.recommend(shape, bg, theme, recommended_palette)
        if np.mean(shape_palette) < 254:
            shape_color = shape_recommender.extract_decor_color(shape_palette)
        else:
            shape_color = (255, 255, 255)
        new = PIL.Image.new(mode="RGB", size=(256,256), color=shape_color)
        target_path = os.path.join(recommended_shape_dir, os.path.basename(shape_file))
        io.imsave(target_path, np.asarray(new))
        # io.imsave(target_path, shape_palette)
    
    for text_file in text_files:
        text = np.asarray(PIL.Image.open(text_file).convert('RGB'))
        text = np.where(text==0, 255, text)
        text = aug(image=text)
        text_palette = text_recommender.recommend(text, bg, theme, recommended_palette)
        if np.mean(text_palette) < 253:
            text_color = text_recommender.extract_decor_color(text_palette)
        else:
            text_color = (0, 0, 0)
        new = PIL.Image.new(mode="RGB", size=(256,256), color=text_color)
        target_path = os.path.join(recommended_text_dir, os.path.basename(text_file))
        io.imsave(target_path, np.asarray(new))
        # io.imsave(target_path, text_palette)
    
    
   
    # print(shape_color)

    # svg_recommender = SvgRecommender(opt, decor, image, bg, theme, 'shape')
    # recolored_image = svg_recommender.recommend()
   
    
# if __name__ == '__main__':
#     from de_stijl.backend.modules.options import Options
#     def is_image_file(filename):
#         return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])

#     opt = Options().parse()
#     root_path = './mockdata/templates/template01'
#     target_dir = './mockdata/templates/shape_tmp'

#     image_path = f'{root_path}/palette_gt.png'
#     bg_path = f'{root_path}/bg.png'
#     theme_path = f'{root_path}/theme.png'
#     shape_dir = f'{root_path}/v1/shapes/'
#     text_dir = f'{root_path}/v1/texts/'
#     shape_gt_dir = f'{root_path}/v2/'
#     text_gt_dir = f'{root_path}/v2/'

#     aug = iaa.Grayscale(alpha=1.0)
#     resize_aug = iaa.Resize(256, interpolation='cubic')

#     image = np.asarray(PIL.Image.open(image_path).convert('RGB'))
#     bg = np.asarray(PIL.Image.open(bg_path).convert('RGB'))
#     bg = resize_aug(image=bg)
#     theme = np.asarray(PIL.Image.open(theme_path).convert('RGB'))

    
#     shape_files = [os.path.join(shape_dir, x) for x in os.listdir(shape_dir) if is_image_file(x)]
#     text_files = [os.path.join(text_dir, x) for x in os.listdir(text_dir) if is_image_file(x)]

#     for idx, shape_file in enumerate(shape_files):
#         gt_path = os.path.join(shape_gt_dir, os.path.basename(shape_file))
#         shape_gt = np.asarray(PIL.Image.open(gt_path).convert('RGB'))
#         shape = np.asarray(PIL.Image.open(shape_file).convert('RGB'))
#         shape_gt = np.where(shape_gt==0, 255, shape_gt)
#         shape = np.where(shape==0, 255, shape)

#         shape = resize_aug(image=shape)
#         shape_gt = resize_aug(image=shape_gt)

#         shape = aug(image=shape)
        
#         target_path = os.path.join(target_dir, os.path.basename(shape_file))
#         output = np.hstack((shape, theme, bg, image, shape_gt))
#         io.imsave(target_path, output)
#         # io.imsave(target_path, shape_palette)
    
#     for idx, shape_file in enumerate(text_files):
#         gt_path = os.path.join(text_gt_dir, os.path.basename(shape_file))
#         shape_gt = np.asarray(PIL.Image.open(gt_path).convert('RGB'))
#         shape = np.asarray(PIL.Image.open(shape_file).convert('RGB'))
#         shape_gt = np.where(shape_gt==0, 255, shape_gt)
#         shape = np.where(shape==0, 255, shape)

#         shape = resize_aug(image=shape)
#         shape_gt = resize_aug(image=shape_gt)

#         shape = aug(image=shape)
        
#         target_path = os.path.join(target_dir, os.path.basename(shape_file))
#         output = np.hstack((shape, theme, bg, image, shape_gt))
#         io.imsave(target_path, output)   
