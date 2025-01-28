#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
# DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
DATASET=/app/data # end of life data

# PRETRAINED_MODEL=/home/oweng/fastml-science/sensor-data-compression/training/quantized-6bit-end-of-life/8x8_c8_S2_tele_qK_6bit/8x8_c8_S2_tele_qK_6bit.hdf5 # must be absolute path
PRETRAINED_MODEL=/app/dev/training/quantized-6bit-end-of-life/8x8_c8_S2_tele_qK_6bit/8x8_c8_S2_tele_qK_6bit.hdf5 # must be absolute path
MODEL=8x8_c8_S2_tele_qK_6bit

OUTPUT_DIR=./pynq_z2
INPUT_DATA_TB="${OUTPUT_DIR}/hgcal_test_input.npy"
OUTPUT_DATA_TB="${OUTPUT_DIR}/hgcal_test_output.npy"

python3 convert.py \
	-i $DATASET \
	-o $OUTPUT_DIR \
	--AEonly 1 \
	--nELinks 5 \
	--models $MODEL \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--input_data_tb $INPUT_DATA_TB \
	--output_data_tb $OUTPUT_DATA_TB
