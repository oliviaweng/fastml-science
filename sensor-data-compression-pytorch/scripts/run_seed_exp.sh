#!/bin/bash

CUDA_DEVICE=$1
SEEDS_FILE=$2

T0=50
WD=0.01
LR=0.001
BATCH=512
NUM_DENSE_FEAT=128

for i in `cat ${SEEDS_FILE}`; do
EXP_NAME="hgcal_dense_float${i}"
CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
    --data_dir ../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file ../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./mlp128_bn_wd_cos_restarts_random_seed_exp \
    --experiment_name $EXP_NAME \
    --max_epochs 100 \
    --seed $i \
    --train \
    --accelerator gpu \
    --learning_rate $LR \
    --dense_only \
    --num_dense_feat $NUM_DENSE_FEAT \
    --batch_size $BATCH \
    --batchnorm \
    --weight_decay $WD \
    --cos_anneal_warm_restarts \
    --warm_restart_freq $T0 \

done