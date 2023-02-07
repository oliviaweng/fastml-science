python3 autoencoder_trainer.py \
    --data_dir /app/data/hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file /app/data/hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./pt_train \
    --experiment_name pt_autoencoder_hgcal \
    --max_epochs 100 \
    --train 
    # --fast_dev_run \