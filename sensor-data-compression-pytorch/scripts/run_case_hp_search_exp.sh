#!/bin/bash

CUDA_DEVICE=$1
LR=$2
WD=$3
T0=$4
BATCH=$5

SEED=567798408
QRELU_BITS=3
QID_BITS=4
QINPUT_BITS=6

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
CKPT="./no_relu_random_seed_exp/hgcal_float${SEED}/last.ckpt"
SAVE_DIR=./quant${SEED}_qr${QRELU_BITS}_qi${QID_BITS}_qinp${QINPUT_BITS}_hp_search
EXP_NAME="hgcal_lr${LR}_wd${WD}_t0${T0}_batch${BATCH}"
EPOCHS=500


BREVITAS_IGNORE_MISSING_KEYS=1 CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
   --data_dir $DATA_DIR \
   --data_file $DATA_FILE \
   --save_dir $SAVE_DIR \
   --experiment_name $EXP_NAME \
   --max_epochs $EPOCHS \
   --seed $SEED \
   --train \
   --checkpoint $CKPT \
   --quantize_act \
   --act1_bitwidth $QRELU_BITS \
   --act2_bitwidth $QID_BITS \
   --quantize_input \
   --qinput_bitwidth $QINPUT_BITS \
   --accelerator gpu \
   --batchnorm \
   --learning_rate $LR \
   --weight_decay $WD \
   --cos_anneal_warm_restarts \
   --warm_restart_freq $T0 \
   --batch_size $BATCH \
