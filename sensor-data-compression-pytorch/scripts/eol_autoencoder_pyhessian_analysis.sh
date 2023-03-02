#!/bin/bash
python3 autoencoder_pyhessian_analysis.py \
    --data_dir /app/data/hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file /app/data/hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --batch_size 5000 \
    --cuda \
    --model-tag eol2_single_batch5000\
    --checkpoint ./pt_train/named_layers_autoencoder_hgcal2/last.ckpt \
    --logfile ./logs/autoencoder_mean_hessian_trace.csv