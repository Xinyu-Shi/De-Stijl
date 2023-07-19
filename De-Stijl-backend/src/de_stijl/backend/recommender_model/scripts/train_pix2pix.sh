#!/bin/bash
set -ex

python train.py \
    --dataroot /home/xinyushi/ads-colorizer/ads_data/image_recommender_dataset03 \
    --name image_recommender_user_study \
    --model pix2pix \
    --netD pixel \
    --netG unet_256 \
    --direction AtoB \
    --lambda_L1 100 \
    --dataset_mode aligned \
    --norm batch \
    --pool_size 0 \
    --n_epochs 500 \
    --n_epochs_decay 2500 \
    --epoch_count 1 \
    --batch_size 16 \

