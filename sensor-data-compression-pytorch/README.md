# Encoder
Training PyTorch ECON-T autoencoder model

This repo is based on the work done here https://github.com/cmantill/Ecoder which was accomplished using the original repo found here (https://github.com/kakwok/Ecoder).

## Download the data
Download the dataset. Right now we're only using the `nElinks_5` dataset:
* [Hgcal dataset](https://emdhgcalae.nrp-nautilus.io/ttbar/data/HGCal22Data_signal_driven_ttbar_v11/nElinks_5/)
* [Elegun dataset](https://emdhgcalae.nrp-nautilus.io/EleGun/low_pt_high_eta/data/nElinks_5/)


## Setup
We provide both `conda` and `Docker` environments for development.
It is up to the user to decide which they prefer, though we recommend conda for easier CUDA setup.

### Conda
We use [Miniforge](https://github.com/conda-forge/miniforge) to manage our conda environment.

Once miniforge is installed, build the environment:
```
mamba env create -f environment.yml
```
We recommend using `mamba` because it is significantly faster at solving the environment than `conda` is.

Activate the environment:
```
conda activate auto
```
and begin developing!

When you are finished, deactivate the environment:
```
conda deactivate auto
```

### Docker
Our image is defined in `./Dockerfile`.
The only line you may need to change is 
```
RUN adduser -u 1000 --disabled-password --gecos "" --shell /bin/bash appuser && \
    chown -R appuser /app/
```
and change `1000` to your user's UID. To find you UID, run `id -u YOUR_USERNAME`.

We use docker compose to manage our docker instance. The lines you may need to change are
```yaml
- '../../hgcal22data_signal_driven_ttbar_v11:/app/data/hgcal22data_signal_driven_ttbar_v11'
- '../../elegun-low-pt-high-eta:/app/data/elegun-low-pt-high-eta'
```
where you need to update these lines to 
```yaml
- 'YOUR_HGCAL_DATASET_PATH:/app/data/hgcal22data_signal_driven_ttbar_v11'
- 'YOUR_ELEGUN_DATASET_PATH:/app/data/elegun-low-pt-high-eta'
```

Then run 
```
./docker-build.sh
```
which will build the docker image and spin up an instance.

You only need to build the image once. If you kill the instance and want to spin it up again, make sure you're in the same directory as `docker-compose.yml` and run
```
docker-compose up -d
```

Access your docker container by running:
```
docker exec -it autoencoder bash
```

## Process the data
The dataset requires a bit of preprocessing, which is pretty slow. 
You will likely need to adjust the paths and directories according to your system.
To pre-process the data and save it, run
```
./scripts/process_data.sh
```
And this will save your data in your data directories as pickled `.npy` files. 
You will need to run this script once for the Hgcal dataset and once for the elegun dataset (by updating the appropriate data directory paths in the `process_data.sh` script).


## Training ECON-T autoencoder
We provide scripts for training. 
You will likely need to adjust the paths and directories according to your system.
To train the autoencoder on the hgcal dataset, run
```
./scripts/train_eol_pt_autoencoder.sh
```

To train the autoencoder on the elegun dataset, run
```
./scripts/train_bol_pt_autoencoder.sh
```

We use Tensorboard to monitor our training sessions. In a separate tmux window/session, run
```
./scripts/tensorboard.sh
```
and in your local web browser, open `localhost:6006` to view the training logs.


