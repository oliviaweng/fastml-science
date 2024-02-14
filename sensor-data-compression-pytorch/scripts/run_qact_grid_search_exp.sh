#!/bin/bash

CUDA_DEVICE=$1
QRELU_BITS=$2
QID_BITS=$3

T0=50
WD=0.01
LR=0.001
BATCH=512
QINPUT_BITS=6
SEED=1523643930
NUM_DENSE_FEAT=128

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
CKPT="./mlp128_bn_wd_cos_restarts_random_seed_exp/hgcal_dense_float${SEED}/last.ckpt"
SAVE_DIR=./dense_qact_grid_search_500epochs
EXP_NAME="hgcal_dense_qact${SEED}_qr${QRELU_BITS}_qi${QID_BITS}"
EPOCHS=500


BREVITAS_IGNORE_MISSING_KEYS=1 CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
   --data_dir $DATA_DIR \
   --data_file $DATA_FILE \
   --save_dir $SAVE_DIR \
   --experiment_name $EXP_NAME \
   --max_epochs $EPOCHS \
   --seed $SEED \
   --train \
   --accelerator gpu \
   --checkpoint $CKPT \
   --quantize_input \
   --qinput_bitwidth $QINPUT_BITS \
   --quantize_act \
   --act1_bitwidth $QRELU_BITS \
   --act2_bitwidth $QID_BITS \
   --learning_rate $LR \
   --dense_only \
   --num_dense_feat $NUM_DENSE_FEAT \
   --batch_size $BATCH \
   --batchnorm \
   --weight_decay $WD \
   --cos_anneal_warm_restarts \
   --warm_restart_freq $T0 \