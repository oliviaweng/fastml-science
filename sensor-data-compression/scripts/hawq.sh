#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-small-econ-qkeras-end-of-life/run3-row27-small-econ-qkeras/run3-row27-small-econ-qkeras.hdf5 # must be absolute path
PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-big-econ-qkeras-end-of-life/run5-row21-big-econ-qkeras/run5-row21-big-econ-qkeras.hdf5 # must be absolute path
OUTPUT_DIR=hawq


CUDA_VISIBLE_DEVICES="" python3 hawq_encoder.py \
	-i $DATASET \
	-o ${OUTPUT_DIR} \
	--AEonly 1 \
	--nELinks 5 \
	--models run5-row21-big-econ-qkeras \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--num_val_inputs 32