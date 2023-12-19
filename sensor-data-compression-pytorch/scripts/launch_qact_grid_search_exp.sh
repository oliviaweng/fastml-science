#!/bin/bash

for qid in `seq 2 1 4`; do
for qrelu in `seq 2 1 4`; do
    command="\"source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 ${qrelu} ${qid}\""
    echo $command
done
done
tmux new-session -d -s g00 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 2 2"
tmux new-session -d -s g01 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 3 2"
tmux new-session -d -s g02 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 4 2"
tmux new-session -d -s g03 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 2 3"
tmux new-session -d -s g04 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 3 3"

# tmux new-session -d -s g05 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 4 3"
# tmux new-session -d -s g06 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 2 4"
# tmux new-session -d -s g07 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 3 4"
# tmux new-session -d -s g08 "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 4 4"


# tmux new-session -d -s g00  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 2 2"
# tmux new-session -d -s g01  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 4 2"
# tmux new-session -d -s g02  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 6 2"
# tmux new-session -d -s g03  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 8 2"
# tmux new-session -d -s g04  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 2 4"
# tmux new-session -d -s g05  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 1 4 4"
# tmux new-session -d -s g06  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 6 4"
# tmux new-session -d -s g07  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 2 8 4"


# tmux new-session -d -s g08  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 2 6"
# tmux new-session -d -s g09  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 4 6"
# tmux new-session -d -s g10  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 6 6"
# tmux new-session -d -s g11  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 8 6"
# tmux new-session -d -s g12  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 2 8"
# tmux new-session -d -s g13  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 4 8"
# tmux new-session -d -s g14  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 6 8"
# tmux new-session -d -s g15  "source ~/.bash_profile; conda activate auto; ./scripts/run_qact_grid_search_exp.sh 0 8 8"

# tmux kill-session -t g00  
# tmux kill-session -t g01  
# tmux kill-session -t g02  
# tmux kill-session -t g13  
# tmux kill-session -t g14  
# tmux kill-session -t g15  
# tmux kill-session -t g16  
# tmux kill-session -t g17  
# tmux kill-session -t g18  
# tmux kill-session -t g19  
# tmux kill-session -t g210 
# tmux kill-session -t g211 
# tmux kill-session -t g212 
# tmux kill-session -t g213 
# tmux kill-session -t g214 