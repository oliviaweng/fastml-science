#!/bin/bash

CUDA_DEVICE=$1
NUM_DENSE_FEAT=$2
LR=$3
WD=$4
T0=$5
BATCH=$6


SEED=1
# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
SAVE_DIR=./mlp_float_bn_wd_cos_restarts
EXP_NAME="hgcal_mlp_float${SEED}_dense_feat${NUM_DENSE_FEAT}_lr${LR}_wd${WD}_lrt0${T0}_batch${BATCH}"
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
   --learning_rate $LR \
   --dense_only \
   --num_dense_feat $NUM_DENSE_FEAT \
   --batch_size $BATCH \
   --batchnorm \
   --weight_decay $WD \
   --cos_anneal_warm_restarts \
   --warm_restart_freq $T0 \