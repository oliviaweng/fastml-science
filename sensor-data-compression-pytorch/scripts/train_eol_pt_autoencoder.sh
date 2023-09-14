CUDA_VISIBLE_DEVICES=1 python3 autoencoder_trainer.py \
    --data_dir ../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ \
    --data_file ../../hgcal22data_signal_driven_ttbar_v11/hgcal22data_signal_driven_ttbar_v11_nELinks5.npy \
    --save_dir ./brevitas \
    --experiment_name test \
    --max_epochs 100 \
    --seed 1 \
    --train \
    --accelerator gpu \
    # --devices "[1]" \
    # --fast_dev_run \