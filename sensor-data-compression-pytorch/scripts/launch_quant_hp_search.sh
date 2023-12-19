#!/bin/bash

qinp=7
for qid in `seq 3 1 4`; do
for qrelu in `seq 2 1 4`; do
    if [[ "$qid" == '3' && "$qrelu" == '2' ]]; then
        continue
    fi
    command="\"source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 0 567798408 ${qrelu} ${qid} ${qinp}\""
    echo $command
done
done

tmux new-session -d -s q00 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 0 567798408 3 3 7"
tmux new-session -d -s q01 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 4 3 7"
tmux new-session -d -s q02 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 2 4 7"
tmux new-session -d -s q03 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 3 4 7"
tmux new-session -d -s q04 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 2 567798408 4 4 7"

# tmux new-session -d -s q00 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 0 567798408 3 3 8"
# tmux new-session -d -s q01 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 0 567798408 4 3 8"
# tmux new-session -d -s q02 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 0 567798408 2 4 8"
# tmux new-session -d -s q13 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 3 4 8"
# tmux new-session -d -s q14 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 4 4 8"

# tmux new-session -d -s q15 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 1 567798408 3 3 6"
# tmux new-session -d -s q26 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 2 567798408 4 3 6"
# tmux new-session -d -s q27 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 2 567798408 2 4 6"
# tmux new-session -d -s q28 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 2 567798408 3 4 6"
# tmux new-session -d -s q29 "source ~/.bash_profile; conda activate auto; ./scripts/run_quant_hp_search_exp.sh 2 567798408 4 4 6"

# tmux kill-session -t q00  
# tmux kill-session -t q01  
# tmux kill-session -t q02  
# tmux kill-session -t q03  
# tmux kill-session -t q04  
# tmux kill-session -t q05  
# tmux kill-session -t q06  
# tmux kill-session -t q07  
# tmux kill-session -t q08  