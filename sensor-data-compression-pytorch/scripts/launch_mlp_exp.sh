#!/bin/bash

lrs=(0.001 0.0005)
t0s=(50)
wds=(0.01 0.1) 
batches=(512)
num_dense_feats=(32 64 128)

for lr in ${lrs[@]}; do 
for t0 in ${t0s[@]}; do
for wd in ${wds[@]}; do 
for batch in ${batches[@]}; do
for n in ${num_dense_feats[@]}; do
    command="\"source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 0 ${n} ${lr} ${wd} ${t0} ${batch}\""
    echo $command
done
done
done
done
done


# tmux new-session -d -s m00 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 0 32 0.001 0.01 50 512"
tmux new-session -d -s m01 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 0 64 0.001 0.01 50 512"
tmux new-session -d -s m02 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 0 128 0.001 0.01 50 512"
tmux new-session -d -s m03 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 0 32 0.001 0.1 50 512"
tmux new-session -d -s m04 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 1 64 0.001 0.1 50 512"
tmux new-session -d -s m05 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 1 128 0.001 0.1 50 512"
tmux new-session -d -s m06 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 1 32 0.0005 0.01 50 512"
tmux new-session -d -s m07 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 1 64 0.0005 0.01 50 512"
tmux new-session -d -s m08 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 2 128 0.0005 0.01 50 512"
tmux new-session -d -s m09 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 2 32 0.0005 0.1 50 512"
tmux new-session -d -s m10 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 2 64 0.0005 0.1 50 512"
tmux new-session -d -s m11 "source ~/.bash_profile; conda activate auto; ./scripts/run_mlp_exp.sh 2 128 0.0005 0.1 50 512"


