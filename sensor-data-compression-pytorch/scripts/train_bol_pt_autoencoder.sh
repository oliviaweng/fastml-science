python3 autoencoder_trainer.py \
    --data_dir /app/data/elegun-low-pt-high-eta/nElinks_5/ \
    --data_file /app/data/elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy \
    --save_dir ./pt_train \
    --experiment_name named_layers_autoencoder_elegun1 \
    --max_epochs 100 \
    --train 
    # --fast_dev_run \