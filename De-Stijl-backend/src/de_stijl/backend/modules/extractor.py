import scipy
import numpy as np
import PIL
import imgaug.augmenters as iaa
from skimage.segmentation import slic
from skimage.measure import regionprops
from skimage import io, color
import sklearn.cluster

class Extractor():
    def __init__(self, opt):
        self.ncolors = opt.ncolors
        if opt.ncolors == 'more':
            self.slic_segments = 25
            self.proportion = 6
        elif opt.ncolors == 'less':
            self.slic_segments = 8
            self.proportion = 4
        else:
            self.slic_segments = 16
            self.proportion = 5
        
        self.slic_compactness = opt.slic_compactness
        self.color_type = opt.color_type

    def __paint_region(self, image, rp, color):
        for i in range(rp.shape[0]):
            image[rp[i][0]][rp[i][1]][:] = color[:]
    
    def __find_dominant_color(self, pixels):
        kmeans = sklearn.cluster.MiniBatchKMeans(
            n_clusters=3,
            init="k-means++",
            max_iter=10,
            random_state=1000
        ).fit(pixels)
        codes = kmeans.cluster_centers_
        vecs, _dist = scipy.cluster.vq.vq(pixels, codes)        
        counts, _bins = np.histogram(vecs, len(codes))    

        colors = []
        for idx in np.argsort(counts)[::-1]:
            colors.append(tuple([int(code) for code in codes[idx]]))
    
        return colors[0]

    def extract(self, image):
        image = np.asarray(PIL.Image.fromarray(image).convert('RGB'))
        resize_aug = iaa.Resize(256, interpolation='cubic')
        resized_image = resize_aug(image=image)
        resized_image = PIL.Image.fromarray(resized_image)
        # resized_image = resized_image.convert('RGBA')
        pixels = resized_image.getdata()
        transparent_pixels = []
        for pixel in pixels:
            if np.sum(pixel[:3]) < 45:
                transparent_pixels.append((255,255,255))
            else:
                transparent_pixels.append(pixel)
        resized_image.putdata(transparent_pixels)
        resized_image = np.array(resized_image)
        superpixels = slic(
            resized_image, 
            n_segments=self.slic_segments, 
            compactness=self.slic_compactness, 
            enforce_connectivity=True, 
            convert2lab=True, 
            start_label=1
        )
        regions = regionprops(superpixels, intensity_image=resized_image[:,:,:3])
        for r in regions:
            all_pixels = []
            for i in range(r.coords.shape[0]):
                all_pixels.append(resized_image[r.coords[i][0]][r.coords[i][1]][:])
            all_pixels = np.asarray(all_pixels)

            if self.color_type == 'dominant':
                color = self.__find_dominant_color(all_pixels)
            else:
                color = r.mean_intensity
            self.__paint_region(resized_image, r.coords, color)

        palette = resized_image[:, :, :3]
        aug_seq = iaa.Sequential([
            iaa.Resize(self.proportion, interpolation='nearest'),
            iaa.Resize(256, interpolation='nearest'),
        ])
        palette = aug_seq(image=palette)
        return palette

    
# test
if __name__ == '__main__':
    from de_stijl.backend.modules.options import Options
    opt = Options().parse()
    root_path = './mockdata/templates/template06'
    file = f'{root_path}/v1/image_01.png'
    palette_path = f'{root_path}/results/palette_01.png'
    image = np.asarray(PIL.Image.open(file).convert('RGB'))
    image = np.where(image==0, 255, image)
    # image = np.where(image==0, 255, image)
    # resize = iaa.Resize(256, interpolation='cubic')
    # image = resize(image=image)
    extractor = Extractor(opt)
    palette = extractor.extract(image)
    io.imsave(palette_path, palette)

# if __name__ == '__main__':
#     from de_stijl.backend.modules.options import Options
#     opt = Options().parse()
#     root_path = './mockdata/templates/template06'
#     lq_file = f'{root_path}/v1/image_01.png'
#     gt_file = f'{root_path}/v2/image_01.png'
#     bg_path = f'{root_path}/bg.png'
#     theme_path = f'{root_path}/theme.png'

#     target_path = f'{root_path}/palette_gt.png'
#     # gt_palette_path = f'{root_path}/results/palette_01.png'
#     # lq_image = np.asarray(PIL.Image.open(lq_file).convert('RGB'))
#     gt_image = np.asarray(PIL.Image.open(gt_file).convert('RGB'))
#     gt_image = np.where(gt_image==0, 255, gt_image)
#     # bg = np.asarray(PIL.Image.open(bg_path).convert('RGB'))
#     # theme = np.asarray(PIL.Image.open(theme_path).convert('RGB'))
#     extractor = Extractor(opt)
#     # lq_palette = extractor.extract(lq_image)
#     gt_palette = extractor.extract(gt_image)

#     # resize = iaa.Resize(256, interpolation='nearest')
#     # bg = resize(image=bg)
#     # output = np.hstack((lq_palette, theme, bg, theme, gt_palette))
#     io.imsave(target_path, gt_palette)



