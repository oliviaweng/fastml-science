#!/bin/bash

CUDA_DEVICE=$1
SEED=$2
QRELU_BITS=$3
QID_BITS=$4
QINPUT_BITS=$5

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
CKPT="./brevitas_qinput_float_model/hgcal_float${SEED}_qinput${QINPUT_BITS}/last.ckpt"
SAVE_DIR=./eval
EXP_NAME="hgcal_qact${SEED}"


BREVITAS_IGNORE_MISSING_KEYS=1 CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python3 autoencoder_trainer.py \
    --data_dir $DATA_DIR \
    --data_file $DATA_FILE \
    --save_dir $SAVE_DIR \
    --experiment_name $EXP_NAME \
    --seed $SEED \
    --checkpoint $CKPT \
    --accelerator gpu \
    --evaluate \
    --quantize_input \
    --qinput_bitwidth $QINPUT_BITS \
    # --quantize_act \
    # --qrelu_bitwidth $QRELU_BITS \
    # --qidentity_bitwidth $QID_BITS \
