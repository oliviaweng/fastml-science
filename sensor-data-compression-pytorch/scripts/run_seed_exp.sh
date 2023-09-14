#!/bin/bash

CUDA_DEVICE=$1
SEEDS_FILE=$2

for i in `cat ${SEEDS_FILE}`; do
EXP_NAME="hgcal_float${i}"
CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
    --data_dir ../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file ../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./random_seed_exp \
    --experiment_name $EXP_NAME \
    --max_epochs 100 \
    --seed $i \
    --train \
    --accelerator gpu \

done