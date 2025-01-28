#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-small-econ-hawq-end-of-life/run3-row27-small-econ/run3-row27-small-econ.hdf5
MODEL=run3-row27-small-econ

OUTPUT_DIR=./stat_fi

python3 stat_fi.py \
	-i $DATASET \
	-o $OUTPUT_DIR \
	--AEonly 1 \
	--nELinks 5 \
	--models $MODEL \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
