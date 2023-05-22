#!/bin/bash

# DATASET=../../elegun-low-pt-high-eta/nElinks_5 # begin of life data
DATASET=../../hgcal22data_signal_driven_ttbar_v11/nElinks_5/ # end of life data
PRETRAINED_MODEL=/home/anmeza/GitHub/fastml-science/sensor-data-compression/training/fkeras-6bit-end-of-life/8x8_c8_S2_tele_fqK_6bit/8x8_c8_S2_tele_fqK_6bit.hdf5
OUTPUT_DIR=faulty-eval/sampling-ber1e-4-test
LOGFILE=/home/anmeza/GitHub/fastml-science/sensor-data-compression/faulty-eval/end-of-life-emd-sampling-ber1e-4-test.csv
IEU_EFX_DIR="/home/anmeza/GitHub/FKeras-Experiments/data"

#bits=12720

model_id=$1
vinputs=$2
vsystem=$3 
lbi=$4
hbi=$5
git_step=$6

for (( i=$lbi; i<$hbi ; i++ )); do 
echo "Sanity check ber = 0"
python3 iccad_2023_experiment1_ground_truth.py \
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
        --num_val_inputs 20000 \
        --num_hess_inputs 8192 \
        --ieu_model_id $model_id \
        --ieu_vsystem_id $vsystem \
        --ieu_efx_dir $IEU_EFX_DIR \
        --ieu_pefr_name "${model_id}_pefr_vinputs${vinputs}_vsystem${vsystem}_ground_truth.pkl" \
        --ieu_pefd_name "${model_id}_pefd_vinputs${vinputs}_vsystem${vsystem}_ground_truth.pkl" \
        --ieu_git_step $git_step \
        --ieu_lbi $lbi
exit
done