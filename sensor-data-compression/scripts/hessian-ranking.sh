#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data

PATH_PREFIX=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression
OUTPUT_DIR="$PATH_PREFIX/ranked_model_params"
EXTRA_FLAGS=""
BIT_WIDTH=0
MODEL_ID=""
if [ $1 -eq 0 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-6bit-end-of-life/8x8_c8_S2_tele_fqK_6bit/8x8_c8_S2_tele_fqK_6bit.hdf5
	MODEL_NAME=8x8_c8_S2_tele_fqK_6bit
	BIT_WIDTH=6
	MODEL_ID="ECONT-baseline"
elif [ $1 -eq 1 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-small-econ-hawq-end-of-life/run3-row27-small-econ/run3-row27-small-econ.hdf5
	MODEL_NAME=run3-row27-small-econ
	BIT_WIDTH=8
	MODEL_ID="ECONT-small-pareto"
elif [ $1 -eq 2 ]; then
	PRETRAINED_MODEL=$PATH_PREFIX/training/fkeras-big-econ-hawq-end-of-life/run5-row21-big-econ/run5-row21-big-econ.hdf5
	MODEL_NAME=run5-row21-big-econ
	EXTRA_FLAGS="--layer_precision_info '[(800,5),(8192,7)]'"
	MODEL_ID="ECONT-large-pareto"

else
	echo "Error"
fi

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
	--bit_width $BIT_WIDTH \
	--model_id $MODEL_ID \
	$EXTRA_FLAGS
