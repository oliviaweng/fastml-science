#!/bin/bash

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
SAVE_DIR=./brevitas
SEED=3
EXP_NAME="autoencoder_hgcal_qact${SEED}"
EPOCHS=100

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
