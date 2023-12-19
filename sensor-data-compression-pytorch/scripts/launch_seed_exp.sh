#!/bin/bash

tmux new-session -d -s r00 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 0 ./random_seeds/random_seeds0.txt"
tmux new-session -d -s r01 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 0 ./random_seeds/random_seeds1.txt"
tmux new-session -d -s r02 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 0 ./random_seeds/random_seeds2.txt"
tmux new-session -d -s r03 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 1 ./random_seeds/random_seeds3.txt"
tmux new-session -d -s r04 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 1 ./random_seeds/random_seeds4.txt"
# tmux new-session -d -s r05 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 1 ./random_seeds/random_seeds5.txt"
# tmux new-session -d -s r06 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 1 ./random_seeds/random_seeds6.txt"
# tmux new-session -d -s r07 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 2 ./random_seeds/random_seeds7.txt"
# tmux new-session -d -s r08 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 2 ./random_seeds/random_seeds8.txt"
# tmux new-session -d -s r09 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 2 ./random_seeds/random_seeds9.txt"
# tmux new-session -d -s r210 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 2 ./random_seeds/random_seeds10.txt"
# tmux new-session -d -s r211 "source ~/.bash_profile; conda activate auto; ./scripts/run_seed_exp.sh 2 ./random_seeds/random_seeds11.txt"


# tmux kill-session -t r00
# tmux kill-session -t r01
# tmux kill-session -t r02
# tmux kill-session -t r03
# tmux kill-session -t r14
# tmux kill-session -t r15
# tmux kill-session -t r16
# tmux kill-session -t r17
# tmux kill-session -t r28
# tmux kill-session -t r29
# tmux kill-session -t r210
# tmux kill-session -t r211

