#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-big-econ-hawq-end-of-life/run5-row21-big-econ/run5-row21-big-econ.hdf5
MODEL=run5-row21-big-econ

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
