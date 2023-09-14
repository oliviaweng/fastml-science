import numpy as np 


NUM_FILES = 12
NUM_SEEDS = 50
FILE_NAME = "random_seeds"

rng = np.random.default_rng(8135801)
rand_nums = rng.integers(0, high=np.iinfo(np.int32).max, size=NUM_SEEDS)

print(f"Rand nums: {rand_nums}")

rand_num_lists = np.array_split(rand_nums, NUM_FILES)

for i, l in enumerate(rand_num_lists):
    file = FILE_NAME + str(i) + ".txt"
    with open(file, "w") as f:
        for n in l:
            f.write(str(n) + "\n")


