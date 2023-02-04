python3 autoencoder_trainer.py \
    --data_dir /app/data/hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file /app/data/hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./pt_eval \
    --experiment_name pt_autoencoder_test \
    --max_epochs 3 \
    --evaluate
    # --fast_dev_run \