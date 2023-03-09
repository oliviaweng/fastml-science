#!/bin/bash
python3 autoencoder_pyhessian_analysis.py \
    --data_dir /app/data/elegun-low-pt-high-eta/nElinks_5/ \
    --data_file /app/data/elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy \
    --batch_size 5000 \
    --cuda \
    --checkpoint ./pt_train/named_layers_autoencoder_elegun2/last.ckpt \
    --model-tag bol2_single_batch5000 \
    --logfile ./logs/autoencoder_mean_hessian_trace.csv
