#!/bin/bash

# 500 epochs
qid=4
qinp=6
qrelu=3

# PREV 0
# lrs=(0.01 0.005)
# t0s=(100 50)
# wds=(0.01 0.001) 
# batches=(512 1024 2048)

# PREV 1
# lrs=(0.01 0.1) 
# t0s=(100 125)  
# wds=(0.01 0.1) 
# batches=(512 1024)

lrs=(0.01 0.001)
t0s=(100 50)
wds=(0.01 0.001) 
batches=(512 1024)
for lr in ${lrs[@]}; do 
for t0 in ${t0s[@]}; do
for wd in ${wds[@]}; do 
for batch in ${batches[@]}; do 
    command="\"source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 ${lr} ${wd} ${t0} ${batch}\""
    echo $command
done
done
done
done

# CURR
tmux new-session -d -s s00 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.01 100 512"
tmux new-session -d -s s01 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.01 100 1024"
tmux new-session -d -s s02 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.001 100 512"
tmux new-session -d -s s03 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.001 100 1024"
tmux new-session -d -s s04 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.01 50 512"

# QUEUE
# tmux new-session -d -s s05 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.01 50 1024"
# tmux new-session -d -s s06 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.001 50 512"
# tmux new-session -d -s s07 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.001 50 1024"
# tmux new-session -d -s s08 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.01 100 512"
# tmux new-session -d -s s09 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.01 100 1024"
# tmux new-session -d -s s10 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.001 100 512"
# tmux new-session -d -s s11 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.001 100 1024"
# tmux new-session -d -s s12 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.01 50 512"
# tmux new-session -d -s s13 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.01 50 1024"
# tmux new-session -d -s s14 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.001 50 512"
# tmux new-session -d -s s15 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.001 0.001 50 1024"


# DONE
# tmux new-session -d -s s00 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.01 100 512"
# tmux new-session -d -s s01 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.01 100 1024"
# tmux new-session -d -s s02 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.01 100 2048"
# tmux new-session -d -s s03 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.001 100 512"
# tmux new-session -d -s s04 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.001 100 1024"
# tmux new-session -d -s s01 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.01 50 512"
# tmux new-session -d -s s02 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.01 50 1024"
# tmux new-session -d -s s03 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.001 50 512"
# tmux new-session -d -s s04 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.001 50 1024"
# tmux new-session -d -s s05 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.005 0.01 100 512"
# tmux new-session -d -s s06 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.005 0.01 100 1024"
# tmux new-session -d -s s07 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.005 0.001 100 512"
# tmux new-session -d -s s08 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.005 0.001 100 1024"
# tmux new-session -d -s s09 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.005 0.01 50 512"
# tmux new-session -d -s s10 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.005 0.01 50 1024"
# tmux new-session -d -s s21 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.005 0.001 50 512"
# tmux new-session -d -s s22 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.005 0.001 50 1024"
# tmux new-session -d -s s01 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.01 100 512"
# tmux new-session -d -s s02 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.01 100 1024"
# tmux new-session -d -s s03 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 0 0.01 0.1 100 512"
# tmux new-session -d -s s04 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.1 100 1024"
# tmux new-session -d -s s05 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.01 125 512"
# tmux new-session -d -s s06 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 1 0.01 0.01 125 1024"
# tmux new-session -d -s s07 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.1 125 512"
# tmux new-session -d -s s08 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.01 0.1 125 1024"
# tmux new-session -d -s s09 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.1 0.01 100 512"
# tmux new-session -d -s s10 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.1 0.01 100 1024"
# tmux new-session -d -s s11 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.1 0.1 100 512"
# tmux new-session -d -s s12 "source ~/.bash_profile; conda activate auto; ./scripts/run_case_hp_search_exp.sh 2 0.1 0.1 100 1024"
