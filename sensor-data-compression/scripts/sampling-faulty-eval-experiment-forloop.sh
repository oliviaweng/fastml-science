#!/bin/bash

TRIALS=1
# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
# PRETRAINED_MODEL=/home/olivia/xdr/econ-t/fastml-science/sensor-data-compression/training/fkeras-quantized-begin-of-life-all-data/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
# PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-quantized-end-of-life/8x8_c8_S2_tele_fqK/8x8_c8_S2_tele_fqK.hdf5
PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-6bit-end-of-life/8x8_c8_S2_tele_fqK_6bit/8x8_c8_S2_tele_fqK_6bit.hdf5
OUTPUT_DIR=faulty-eval/sampling-ber1e-4-test
LOGFILE=/home/anmeza/GitHub/fastml-science/sensor-data-compression/faulty-eval/end-of-life-emd-sampling-ber1e-4-test.csv

# Sanity check
#bits=10600
bits=12720
VMs=8
system=0
lbi=$((bits/VMs * system))
hbi=$((bits/VMs * system + bits/VMs))
for (( i=$lbi; i<$hbi ; i++ )); do 
echo "Sanity check ber = 0"
python3 sampling_faulty_eval_experiment.py \
        -i $DATASET \
        -o ${OUTPUT_DIR}/ber0 \
        --AEonly 1 \
        --nELinks 5 \
        --models 8x8_c8_S2_tele_fqK_6bit \
        --nrowsPerFile=4500000 \
        --noHeader \
        --pretrained-model $PRETRAINED_MODEL \
        --eval-ber 0 \
        --log-file $LOGFILE \
        --efd_fp "./efd_emd_hesstrace_v0-799999_b${lbi}-${hbi}-forloop.log" \
        --efr_fp "./efr_emd_hesstrace_v0-799999_b${lbi}-${hbi}-forloop.log" \
        --efx_overwrite 0 \
        --use_custom_bfr 1 \
        --bfr_start $i \
        --bfr_end   $((i+1)) \
        --bfr_step  1 \
        --num_val_inputs 800000
done