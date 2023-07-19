import numpy as np
import PIL
from de_stijl.backend.recolorizer_model.test_recolorizer import recolorize_test, load_recolorizer_model
from skimage import io
import imgaug.augmenters as iaa

class Recolorizer():
    def __init__(self, opt):
        self.hint_sparsity = opt.hint_sparsity
        self.model_path = opt.ckpt_dir
        self.model = load_recolorizer_model(self.model_path)

    def __combine_image_and_hints(self, image, palette):
        image = self.__adjust(image)
        aug = iaa.Resize({"height": image.shape[0], "width": image.shape[1]}, interpolation='nearest')
        palette = aug(image=palette)
        return np.hstack((image, palette))

    def __adjust(self, img):
        aug = iaa.RemoveSaturation(0.7)
        img = aug(image=img)
        ow, oh = img.shape[1], img.shape[0]

        # the size needs to be a multiple of this number,
        # because going through generator network may change img size
        # and eventually cause size mismatch error
        mult = 8
        if ow % mult == 0 and oh % mult == 0:
            return img
        w = (ow - 1) // mult
        w = (w + 1) * mult
        h = (oh - 1) // mult
        h = (h + 1) * mult
        resize_aug = iaa.Resize({"height": h, "width": w}, interpolation='cubic')
        return resize_aug(image=img)


    def recolorize(self, image, palette):
        width, height = image.shape[1], image.shape[0]
        compress_aug = iaa.Resize(400, interpolation='cubic')
        recover_aug = iaa.Resize({"height": height, "width": width}, interpolation='cubic')
        image = compress_aug(image=image)
        hints_and_image = self.__combine_image_and_hints(image, palette)
        recolored_image = recolorize_test(hints_and_image, model=self.model, num_points=self.hint_sparsity)
        # change all black pixels to transparent
        recolored_image = PIL.Image.fromarray(recolored_image)
        recolored_image = recolored_image.convert('RGBA')
        pixels = recolored_image.getdata()
        transparent_pixels = []
        for pixel in pixels:
            if np.sum(pixel[:3]) < 130:
                transparent_pixels.append((0,0,0,0))
            else:
                transparent_pixels.append(pixel)
        recolored_image.putdata(transparent_pixels)
        recolored_image = np.array(recolored_image)
        recolored_image = recover_aug(image=recolored_image)
        return recolored_image

# test
if __name__ == '__main__':
    from de_stijl.backend.modules.options import Options
    opt = Options().parse()
    root_path = './mockdata/templates/template05'
    image_path = f'{root_path}/v1/image_01.png'
    # image_path = './mockdata/0548.png'
    palette_path = f'{root_path}/results/test_image_recommender.png'
    # palette_path = './mockdata/0548_palette.png'
    target_path = f'{root_path}/results/test_image_recolorizer.png'
    image = np.asarray(PIL.Image.open(image_path).convert('RGB'))
    palette = np.asarray(PIL.Image.open(palette_path).convert('RGB'))
    recolorizer = Recolorizer(opt)
    recolored_image = recolorizer.recolorize(image, palette)
    io.imsave(target_path, recolored_image)
