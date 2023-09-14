#!/bin/bash

DATA_DIR=$1
DATA_FILE=$2
SAVE_DIR=$3
EXP_NAME=$4
EPOCHS=$5
SEED=$6

python3 autoencoder_trainer.py \
    --data_dir $DATA_DIR \
    --data_file $DATA_FILE \
    --save_dir $SAVE_DIR \
    --experiment_name $EXP_NAME \
    --max_epochs $EPOCHS \
    --seed $SEED \
    --train \
    --quantize_act \
    --accelerator gpu \
    # --fast_dev_run \