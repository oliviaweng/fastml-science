#!/bin/bash
python3 autoencoder_pyhessian_analysis.py \
    --data_dir /app/data/elegun-low-pt-high-eta/nElinks_5/ \
    --data_file /app/data/elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy \
    --batch_size 500 \
    --cuda \
    --checkpoint ./pt_train/named_layers_autoencoder_elegun1/last.ckpt \
    --model-tag bol_single_batch1 \
    --logfile ./logs/autoencoder_mean_hessian_trace.csv
    # --data_dir /app/data/hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    # --data_file /app/data/hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \