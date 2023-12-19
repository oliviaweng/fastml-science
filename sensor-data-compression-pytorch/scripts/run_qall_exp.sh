#!/bin/bash

CUDA_DEVICE=$1
SEED=$2

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
CKPT="./no_relu_random_seed_exp/hgcal_float${SEED}/last.ckpt"
SAVE_DIR=./brevitas_qall_preloaded_wts1
EXP_NAME="hgcal_qall${SEED}"
EPOCHS=100


BREVITAS_IGNORE_MISSING_KEYS=1 CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
    --data_dir $DATA_DIR \
    --data_file $DATA_FILE \
    --save_dir $SAVE_DIR \
    --experiment_name $EXP_NAME \
    --max_epochs $EPOCHS \
    --seed $SEED \
    --train \
    --checkpoint $CKPT \
    --quantize_all \
    --accelerator gpu \