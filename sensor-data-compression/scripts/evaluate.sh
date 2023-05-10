#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-begin-of-life-all-data/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/quantized-6bit-end-of-life/8x8_c8_S2_tele_qK_6bit/8x8_c8_S2_tele_qK_6bit.hdf5 # must be absolute path
OUTPUT_DIR=evaluate


python3 evaluate.py \
	-i $DATASET \
	-o ${OUTPUT_DIR} \
	--AEonly 1 \
	--nELinks 5 \
	--models 8x8_c8_S2_tele_qK_6bit \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--num_val_inputs 810000