CUDA_VISIBLE_DEVICES=0 python3 autoencoder_trainer.py \
    --data_dir /app/data/hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file /app/data/hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./hero-seed-test \
    --experiment_name seed3 \
    --max_epochs 100 \
    --train \
    --seed 3 \
    --accelerator gpu \
