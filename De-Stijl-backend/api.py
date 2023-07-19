import json
from de_stijl.backend.modules.extractor import Extractor
from de_stijl.backend.modules.recommender import Recommender
from de_stijl.backend.modules.recolorizer import Recolorizer
from de_stijl.backend.modules.palette_postprocess import Postprocessor
from de_stijl.backend.modules.options import Options
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from io import BytesIO
import base64
import imgaug.augmenters as iaa

import numpy as np
import PIL 
from skimage import io
import os
import re

import time

opt = Options().parse()
palette_extractor = Extractor(opt)
postprocessor = Postprocessor(opt)
recolorizer = Recolorizer(opt)
image_recommenders = []
theme_levels = [10, 8, 6, 4, 2]
for theme in theme_levels:
    image_recommenders.append(Recommender(opt, ckpt_type='image', theme_level=theme))
shape_recommender = Recommender(opt, ckpt_type='shape')
text_recommender = Recommender(opt, ckpt_type='text')

app = Flask(__name__)
CORS(app)
api = Api(app)
  
class Colorizer(Resource):
    def get(self):
        return {"data": "test connection"}

    def __decode_base64(self, base64_stream):
        image = PIL.Image.open(BytesIO(base64.b64decode(base64_stream))).convert('RGB')
        return np.asarray(image)
    
    def __encode_base64(self, image):
        pil_image = PIL.Image.fromarray(image)
        im_file = BytesIO()
        pil_image.save(im_file, format="PNG")
        im_b64 = base64.b64encode(im_file.getvalue())
        im_b64 = im_b64.decode("utf-8")
        return im_b64
    
    def __decode_HEXcode(self, hex_code):
        rgb = PIL.ImageColor.getcolor(hex_code, "RGB")
        return rgb
    
    def __encode_HEXcode(self, rgb):
        hex_code = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        return hex_code
    
    def __decode_theme_to_image(self, hex_codes):
        img = np.zeros([1, len(hex_codes),3],dtype=np.uint8)
        for idx, hex_code in enumerate(hex_codes):
            rgb = self.__decode_HEXcode(hex_code=hex_code)
            img[0, idx, :] = list(rgb)
        resize_aug = iaa.Resize(256, interpolation='nearest')
        img = resize_aug(image=img)
        return img

    def __read_image_to_b64(self, name, data_root):
        file_name = f'{name}.png'
        path = os.path.join(data_root, file_name)
        image = np.asarray(PIL.Image.open(path).convert('RGB'))
        resize_aug = iaa.Resize(0.05, interpolation='cubic')
        image = resize_aug(image=image)
        print(image.shape)
        im_b64 = self.__encode_base64(image)
        return im_b64

    def __create_mock_data(self):
        data_root = './mockdata/template01/v2'
        bg = self.__read_image_to_b64('bg', data_root)
        canvas_image = self.__read_image_to_b64('canvas_image', data_root)
        images_file_name = ['image_01']
        shapes_file_name = ['shape_01', 'shape_02', 'shape_03','shape_04', 'shape_05', 'shape_06', 'shape_07', 'shape_08', 'shape_09', 'shape_10', 'shape_11']
        texts_file_name = ['text_01', 'text_02', 'text_03']
        
        original_images = []
        shapes = []
        texts = []
        for name in images_file_name:
            element = {
                'ID': name,
                'stream': self.__read_image_to_b64(name, data_root),
            }
            original_images.append(element)
        
        for name in shapes_file_name:
            element = {
                'ID': name,
                'stream': self.__read_image_to_b64(name, data_root),
            }
            shapes.append(element)
        
        for name in texts_file_name:
            element = {
                'ID': name,
                'stream': self.__read_image_to_b64(name, data_root),
            }
            texts.append(element)
        
        input = {
            'canvas_width': '',
            'canvas_height': '',
            'theme': ['#bce4f4', '#f4d43c'],
            'canvas_image': canvas_image,
            'background': bg,
            'original_images': original_images,
            'shapes': shapes,
            'texts': texts,
        }
        # return jsonify(input)
        return input


    def post(self):
        start = time.time()
        print("hello")

        # =======================DEBUG==========================
        # data = self.__create_mock_data()
        # target_theme_path = './mockdata/test_theme.png'
        # target_bg_path = './mockdata/test_bg.png'
        # target_image_path = './mockdata/test_image.png'
        # target_shape_path = './mockdata/test_shape.png'
        # target_palette_path = './mockdata/test_palette.png'
        # target_canvas_path = './mockdata/test_canvas.png'
        # target_recoloried_image_path = './mockdata/test_recolorized_image.png'
        # json_path = './mockdata/request_data.json'
        # with open(json_path, 'r') as f:
        #     data = json.load(f)
        # =======================================================

        res = request.get_json()
        data = res['params']

        image_palettes = []
        shapes = []
        texts = []
        theme_level = data['theme_level']
        canvas_width = data['canvas_width']
        canvas_height = data['canvas_height']
        
        theme = self.__decode_theme_to_image(data['theme'])
        bg = self.__decode_theme_to_image(data['background'])
        gray_scale_aug = iaa.Grayscale(alpha=1.0)

        # ====================== Process Image ======================
        # only support single image case
        image_dict = data['original_images'][1]
        tl = (int(image_dict['coordinates']['tl']['x']), int(image_dict['coordinates']['tl']['y']))
        br = (image_dict['coordinates']['br']['x'], image_dict['coordinates']['br']['y'])
        image_b64 = image_dict['base64Image']
        image_b64 = re.sub('^data:image/.+;base64,', '', image_b64)
        image = self.__decode_base64(image_b64)
        
        palette = palette_extractor.extract(image)
        recommended_palettes = []
        recolored_images = []
        for image_recommender in image_recommenders:
            if image_dict['locked'] == True:
                recommended_palette = palette
            else:
                recommended_palette = image_recommender.recommend(palette, bg, theme, theme)
                recommended_palette = postprocessor.process(palette, recommended_palette)
                recolored_image = recolorizer.recolorize(image, recommended_palette)
                recommended_palette = palette_extractor.extract(recolored_image)
            recommended_palettes.append(recommended_palette)
            recolored_images.append(recolored_image)
        path = './test.png'
        io.imsave(path, recommended_palettes[0])
        # recolorize the image using the specified palette, by default, theme_level = 10
        # recommended_palette = recommended_palettes[int((10 - theme_level) / 2)]
        # recolored_image = recolorizer.recolorize(image, recommended_palette)

        # -----------------------------DEBUG------------------------
        # io.imsave(target_image_path, image)
        # io.imsave(target_palette_path,palette)
        # io.imsave(target_recoloried_image_path, recolored_image)
        # io.imsave(target_theme_path, theme)
        # io.imsave(target_bg_path, bg)
        # -----------------------------------------------------------
        
        palettes_b64 = []
        recolored_images_b64 = []
        for recommended_palette in recommended_palettes:
            palette_b64 = self.__encode_base64(recommended_palette)
            palettes_b64.append(palette_b64)
        for recolored_image in recolored_images:
            recolored_image_b64 = self.__encode_base64(recolored_image)
            recolored_images_b64.append(recolored_image_b64)
        # recolored_image_b64 = self.__encode_base64(recolored_image)
        element = {
            'id': image_dict['id'],
            'coordinates': image_dict['coordinates'],
            'palettes': palettes_b64,
            'recolored_image': recolored_images_b64,
        }
        image_palettes.append(element)
        # ======================End Image Processing=============================

        aug = iaa.Resize({"height": image.shape[0], "width": image.shape[1]}, interpolation='nearest')
        canvas_images = []
        for rec_palette in recommended_palettes:
            canvas_image_pil = PIL.Image.new(mode="RGB", size=(canvas_width, canvas_height), color='white')
            rec_palette_pil = PIL.Image.fromarray(aug(image=rec_palette))
            canvas_image_pil.paste(rec_palette_pil, tl)
            canvas_image = np.asarray(canvas_image_pil)
            canvas_images.append(canvas_image)
        
        
        # ========================== Process Shape =====================
        for shape_dict in data['shapes']:
            shape_b64 = shape_dict['base64Image']
            shape_b64 = re.sub('^data:image/.+;base64,', '', shape_b64)
            shape = self.__decode_base64(shape_b64)
            recommended_color_hexs = []
            for canvas_image in canvas_images:
                if shape_dict['locked'] == True:
                    recommended_color = shape_recommender.extract_decor_color(shape)
                else:
                    recommended_shape = shape_recommender.recommend(gray_scale_aug(image=shape), bg, theme, canvas_image)
                    recommended_color = shape_recommender.extract_decor_color(recommended_shape)
                recommended_color_hex = self.__encode_HEXcode(recommended_color)
                recommended_color_hexs.append(recommended_color_hex)
            element = {
                'id': shape_dict['id'],
                'coordinates': shape_dict['coordinates'],
                'colors': recommended_color_hexs,
            }
            shapes.append(element)
            # new = PIL.Image.new(mode="RGB", size=(256,256), color=recommended_color)
            # io.imsave(target_shape_path, np.asarray(new))
        
        # ========================== Process Text ========================
        for text_dict in data['texts']:
            text_b64 = text_dict['base64Image']
            text_b64 = re.sub('^data:image/.+;base64,', '', text_b64)
            text = self.__decode_base64(text_b64)
            recommended_color_hexs = []
            for canvas_image in canvas_images:
                if text_dict['locked'] == True:
                    recommended_color = text_recommender.extract_decor_color(text)
                else:
                    recommended_text = text_recommender.recommend(gray_scale_aug(image=text), bg, theme, canvas_image)
                    recommended_color = text_recommender.extract_decor_color(recommended_text)
                recommended_color_hex = self.__encode_HEXcode(recommended_color)
                recommended_color_hexs.append(recommended_color_hex)
            
            element = {
                'id': text_dict['id'],
                'coordinates': text_dict['coordinates'],
                'colors': recommended_color_hexs,
            }
            texts.append(element)
        end = time.time()
        print(end - start)  
        output = {
            'image_palettes': image_palettes,
            'shapes': shapes,
            'texts': texts,
            'time': str(end - start),
        }
        print(output)
        response = jsonify(output)
        response.headers.add('Access-Control-Allow-Origin', '*')
            
        return response

class PaletteGenerator(Resource):
    def get(self):
        return {"data": "test connection"}

    def __decode_base64(self, base64_stream):
        image = PIL.Image.open(BytesIO(base64.b64decode(base64_stream))).convert('RGB')
        return np.asarray(image)
    
    def __encode_base64(self, image):
        pil_image = PIL.Image.fromarray(image)
        im_file = BytesIO()
        
        pil_image.save(im_file, format="PNG")
        im_b64 = base64.b64encode(im_file.getvalue())
        
        # remove "b'" in im_b64
        im_b64 = im_b64.decode("utf-8")
        # print(im_b64)
        return im_b64

    def post(self):
        # data = request.get_json()
        res = request.get_json()
        data = res['params']
        # test data
        # image_path = './mockdata/0548.png'
        # image = np.asarray(PIL.Image.open(image_path).convert('RGB'))
        # resize_aug = iaa.Resize(0.1, interpolation='cubic')
        # image = resize_aug(image=image)
        # im_b64 = self.__encode_base64(image)

        im_b64 = data['image']
        im_b64 = re.sub('^data:image/.+;base64,', '', im_b64)
        image = self.__decode_base64(im_b64)

        tl = (int(data['coordinates']['tl']['x']), int(data['coordinates']['tl']['y']))
        br = (data['coordinates']['br']['x'], data['coordinates']['br']['y'])
        canvas_image_pil = PIL.Image.new(mode="RGB", size=(int(br[0]-tl[0]), int(br[1]-tl[1])), color='white')
        image_pil = PIL.Image.fromarray(image)
        canvas_image_pil = image_pil.crop((tl[0], tl[1], br[0], br[1]))
        image = np.asarray(canvas_image_pil)
        
        path = './test.png'
        io.imsave(path, image)
        palette = palette_extractor.extract(image)
        
        palette_base64 = self.__encode_base64(palette)
        output = {
            'palette': str(palette_base64)
        }
        return output


api.add_resource(Colorizer,'/colorizer')
api.add_resource(PaletteGenerator, '/palettegenerator')

  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8001)


    








