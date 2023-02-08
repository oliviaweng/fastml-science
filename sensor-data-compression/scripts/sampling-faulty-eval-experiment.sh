#!/bin/bash

TRIALS=1
# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-begin-of-life-all-data/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-quantized-end-of-life/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
OUTPUT_DIR=faulty-eval/sampling-ber1e-4-test
LOGFILE=/home/anmeza/GitHub/fastml-science/sensor-data-compression/faulty-eval/end-of-life-emd-sampling-ber1e-4-test.csv

# Sanity check
echo "Sanity check ber = 0"
python3 sampling_faulty_eval_experiment.py \
	-i $DATASET \
	-o ${OUTPUT_DIR}/ber0 \
	--AEonly 1 \
	--nELinks 5 \
	--models 8x8_c8_S2_tele_fqK \
	--nrowsPerFile=4500000 \
	--noHeader \
	--pretrained-model $PRETRAINED_MODEL \
	--eval-ber 0 \
	--log-file $LOGFILE

# echo "BER = 1e-4"
# python3 sampling_faulty_eval_experiment.py \
# 	-i $DATASET \
# 	-o ${OUTPUT_DIR}/ber0 \
# 	--AEonly 1 \
# 	--nELinks 5 \
# 	--models 8x8_c8_S2_tele_fqK \
# 	--nrowsPerFile=4500000 \
# 	--noHeader \
# 	--pretrained-model $PRETRAINED_MODEL \
# 	--eval-ber 1e-4 \
# 	--log-file $LOGFILE

# for i in ${BIG_BERS[@]}; do
# 	for t in `seq 1 ${TRIALS}`; do
# 		echo "BER=${i} Trial ${t}"
# 		python3 train.py \
# 		-i $DATASET \
# 		-o ${OUTPUT_DIR}/ber${i} \
# 		--AEonly 1 \
# 		--nELinks 5 \
# 		--models 8x8_c8_S2_tele_fqK \
# 		--nrowsPerFile=4500000 \
# 		--noHeader \
# 		--pretrained-model $PRETRAINED_MODEL \
# 		--eval-ber $i \
# 		--log-file $LOGFILE
# 	done
# done

# for j in `seq 1 ${MIN_BER_EXP}`; do
# 	for t in `seq 1 ${TRIALS}`; do
# 		echo "BER=${j} Trial ${t}"
# 		python3 train.py \
# 		-i $DATASET \
# 		-o ${OUTPUT_DIR}/ber$BER_PREFIX${j} \
# 		--AEonly 1 \
# 		--nELinks 5 \
# 		--models 8x8_c8_S2_tele_fqK \
# 		--nrowsPerFile=4500000 \
# 		--noHeader \
# 		--pretrained-model $PRETRAINED_MODEL \
# 		--eval-ber $BER_PREFIX${j} \
# 		--log-file $LOGFILE
# 	done
# done
