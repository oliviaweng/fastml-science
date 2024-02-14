#!/bin/bash

for qinp in `seq 4 1 11`; do
    command="\"source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh X ${qinp}\""
    echo $command
done

tmux new-session -d -s i00 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh 1 4"
tmux new-session -d -s i01 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh 2 5"
tmux new-session -d -s i02 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh 2 6"
tmux new-session -d -s i03 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh 2 7"
tmux new-session -d -s i04 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh 2 8"

# tmux new-session -d -s i05 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh x 9"
# tmux new-session -d -s i06 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh x 10"
# tmux new-session -d -s i07 "source ~/.bash_profile; conda activate auto; ./scripts/run_qinput_exp.sh X 11"
