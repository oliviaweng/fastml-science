#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

PATH_PREFIX=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression
LAYER_PRECISION_INFO="None"
BIT_WIDTH=0
MODEL_ID=""
if [ $1 -eq 0 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-6bit-end-of-life/8x8_c8_S2_tele_fqK_6bit/8x8_c8_S2_tele_fqK_6bit.hdf5
	MODEL_NAME=8x8_c8_S2_tele_fqK_6bit
	BIT_WIDTH=6
	OUTPUT_DIR="$PATH_PREFIX/ranked_model_bits"
	MODEL_ID="ECONT-baseline"
elif [ $1 -eq 1 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-small-econ-hawq-end-of-life/run3-row27-small-econ/run3-row27-small-econ.hdf5
	MODEL_NAME=run3-row27-small-econ
	BIT_WIDTH=8
	OUTPUT_DIR="$PATH_PREFIX/ranked_model_bits"
	MODEL_ID="ECONT-small-pareto"
elif [ $1 -eq 2 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-big-econ-hawq-end-of-life/run5-row21-big-econ/run5-row21-big-econ.hdf5
	MODEL_NAME=run5-row21-big-econ
	LAYER_PRECISION_INFO="'[(800,5),(8192,7)]'"
	OUTPUT_DIR="$PATH_PREFIX/ranked_model_bits"
	MODEL_ID="ECONT-large-pareto"

else
	echo "Error"
fi

# NUM_VAL_INPUTS=(512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288 800000)

# for i in ${NUM_VAL_INPUTS[@]}; do
python3 hessian_analysis.py \
	-i $DATASET \
	-o ${OUTPUT_DIR} \
	--AEonly 1 \
	--nELinks 5 \
	--models $MODEL_NAME \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--num_val_inputs 512 \
	--bit_width $BIT_WIDTH\
	--layer_precision_info $LAYER_PRECISION_INFO\
	--model_id $MODEL_ID
# done
