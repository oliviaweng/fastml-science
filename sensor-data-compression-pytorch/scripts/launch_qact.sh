#!/bin/bash

# DATA_DIR=../../elegun-low-pt-high-eta/nElinks_5/
# DATA_FILE=../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy
DATA_DIR=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/
DATA_FILE=../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy 
SAVE_DIR=./brevitas
SEED=1
EXP_NAME="autoencoder_hgcal_qact${SEED}"
EPOCHS=100

# for i in `seq 1 3`; do
tmux new-session -d -s qeol1 'source /proj/xlabs/users/olivweng/opt/mambaforge/etc/profile.d/conda.sh ; conda activate auto; sleep infinity'
./scripts/train_pt_autoencoder_qact.sh $DATA_DIR $DATA_FILE $SAVE_DIR $EXP_NAME $EPOCHS $SEED
# done
