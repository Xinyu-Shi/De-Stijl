import scipy
import numpy as np
import PIL
import imgaug.augmenters as iaa
from skimage.segmentation import slic
from skimage.measure import regionprops
from skimage import io, color
import sklearn.cluster

class Postprocessor():
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

    def process(self, original_palette, generated_palette):
        superpixels = slic(
            original_palette, 
            n_segments=self.slic_segments, 
            compactness=self.slic_compactness, 
            enforce_connectivity=True, 
            convert2lab=True, 
            start_label=1
        )
        regions = regionprops(superpixels, intensity_image=generated_palette[:,:,:3])
        for r in regions:
            color = r.mean_intensity
            self.__paint_region(generated_palette, r.coords, color)

        palette = generated_palette[:, :, :3]
        resize_aug = iaa.Resize(32, interpolation='nearest')
        palette = resize_aug(image=palette)
        return palette

if __name__ == '__main__':
    from de_stijl.backend.modules.options import Options
    opt = Options().parse()
    root_path = './mockdata/templates/template05'
    lq_file = f'{root_path}/results/test_image_recommender.png'
    gt_file = f'{root_path}/results/palette_01.png'

    target_path = f'{root_path}/results/post_palette.png'
    # gt_palette_path = f'{root_path}/results/palette_01.png'
    lq_image = np.asarray(PIL.Image.open(lq_file).convert('RGB'))
    gt_image = np.asarray(PIL.Image.open(gt_file).convert('RGB'))
    
    # bg = np.asarray(PIL.Image.open(bg_path).convert('RGB'))
    # theme = np.asarray(PIL.Image.open(theme_path).convert('RGB'))
    processor = Postprocessor(opt)
    # lq_palette = extractor.extract(lq_image)
    post_palette = processor.process(gt_image, lq_image)

    # resize = iaa.Resize(256, interpolation='nearest')
    # bg = resize(image=bg)
    # output = np.hstack((lq_palette, theme, bg, theme, gt_palette))
    io.imsave(target_path, post_palette)



