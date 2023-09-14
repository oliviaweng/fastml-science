python3 autoencoder_trainer.py \
    --data_dir ../../elegun-low-pt-high-eta/nElinks_5/ \
    --data_file ../../elegun-low-pt-high-eta/elegun-low-pt-high-eta_nELinks5.npy \
    --save_dir ./brevitas \
    --experiment_name autoencoder_elegun_float3 \
    --checkpoint ./brevitas/autoencoder_elegun_float3/last.ckpt \
    --evaluate \
    # --fast_dev_run \