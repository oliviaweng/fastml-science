#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-end-of-life/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
OUTPUT_DIR=hessian-analysis

# NUM_VAL_INPUTS=(32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288 800000)

# for i in ${NUM_VAL_INPUTS[@]}; do
python3 hessian_analysis.py \
	-i $DATASET \
	-o ${OUTPUT_DIR} \
	--AEonly 1 \
	--nELinks 5 \
	--models 8x8_c8_S2_tele_fqK \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--num_val_inputs 32
# done
