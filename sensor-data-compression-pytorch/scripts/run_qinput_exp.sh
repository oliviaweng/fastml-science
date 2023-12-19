#!/bin/bash

CUDA_DEVICE=$1
QINPUT_BITS=$2

T0=50
SEED=1
WD=0.01
LR=0.001
BATCH=512
NUM_DENSE_FEAT=128

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
SAVE_DIR=./dense_qinput_float_model
EXP_NAME="hgcal_dense_float${SEED}_qinput${QINPUT_BITS}"
EPOCHS=100


CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
   --data_dir $DATA_DIR \
   --data_file $DATA_FILE \
   --save_dir $SAVE_DIR \
   --experiment_name $EXP_NAME \
   --max_epochs $EPOCHS \
   --seed $SEED \
   --train \
   --accelerator gpu \
   --quantize_input \
   --qinput_bitwidth $QINPUT_BITS \
   --learning_rate $LR \
   --dense_only \
   --num_dense_feat $NUM_DENSE_FEAT \
   --batch_size $BATCH \
   --batchnorm \
   --weight_decay $WD \
   --cos_anneal_warm_restarts \
   --warm_restart_freq $T0 \