import axios from 'axios';

const API_ENDPOINT = "http://127.0.0.1:8001";

interface RecommendationRequest {
    canvas_width?: number;
    canvas_height?: number;
    theme: string[];
    background: string[];
    original_images: any[];
    shapes: any [],
    texts: any[]
}

interface RecommendationResponse {
    entity: {
        image_palettes: [
            {
                ID: string;
                palettes: [string];
                recolored_image: string;
            }
        ];
        shapes: [
            {
                ID: string;
                colors: [string]
            }
        ];
        texts: [
            {
                ID: string;
                colors: [string]
            }
        ];
    }
}

axios.defaults.timeout = 900000;
axios.defaults.headers.post['Content-Type'] ='application/json;';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

export const getColorizerRecommendations = async (req?: RecommendationRequest): Promise<any> => {
    console.log({ params: req })
    return axios.post(`${API_ENDPOINT}/colorizer`, {  params: req })
        .then((res) => {
            return res;
        })
        .catch((err) => {
            console.error(err);
            return err;
        })
}

export const get2DPlatteeGeneration = async (req: any): Promise<any> => {
    console.log({ params: req })
    return axios.post(`${API_ENDPOINT}/palettegenerator`, { params: req })
    .then((res) => {
        return res;
    })
    .catch((err) => {
        console.error(err);
        return err;
    })

}
