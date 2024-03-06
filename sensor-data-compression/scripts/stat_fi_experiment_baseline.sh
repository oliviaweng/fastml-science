#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-6bit-end-of-life/8x8_c8_S2_tele_fqK_6bit/8x8_c8_S2_tele_fqK_6bit.hdf5

MODEL=8x8_c8_S2_tele_fqK_6bit


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
