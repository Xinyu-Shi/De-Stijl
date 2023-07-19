set -ex
python test.py \
    --dataroot /home/xinyushi/ads-colorizer/ads_data/image_recommender_dataset02 \
    --name image_recommender \
    --model pix2pix \
    --netG resnet_6blocks \
    --direction AtoB \
    --dataset_mode aligned \
    --norm batch \
