#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ 
# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-begin-of-life-all-data/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-end-of-life/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
OUTPUT_DIR=training
LOGFILE=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras_pareto_training.csv

MODEL=run3-row27-small-econ
# MODEL=run5-row21-big-econ-qkeras

python3 train.py \
	-i $DATASET \
	-o ${OUTPUT_DIR}/fkeras-small-econ-hawq-end-of-life \
	--AEonly 1 \
	--nELinks 5 \
	--models $MODEL \
	--nrowsPerFile=4500000 \
	--noHeader \
	--log-file $LOGFILE \
	--epochs 100

