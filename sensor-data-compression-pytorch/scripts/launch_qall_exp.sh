#!/bin/bash

tmux new-session -d -s qall00 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 0 567798408"
tmux new-session -d -s qall01 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 0 1908781080"
tmux new-session -d -s qall02 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 0 322576610"
tmux new-session -d -s qall13 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 1 1589076274"
tmux new-session -d -s qall14 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 1 436657949"
tmux new-session -d -s qall15 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 1 1206943242"
tmux new-session -d -s qall26 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 2 126687014"
tmux new-session -d -s qall27 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 2 1193976549"
tmux new-session -d -s qall28 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 2 630442169"
tmux new-session -d -s qall29 "source ~/.bash_profile; conda activate auto; ./scripts/run_qall_exp.sh 2 6849925"
