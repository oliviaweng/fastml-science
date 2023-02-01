import os
import torch
import numpy as np
import pandas as pd
import pytorch_lightning as pl

from utils_pt import normalize

ARRANGE = torch.tensor([
    28,29,30,31,0,4,8,12,
    24,25,26,27,1,5,9,13,
    20,21,22,23,2,6,10,14,
    16,17,18,19,3,7,11,15,
    47,43,39,35,35,34,33,32,
    46,42,38,34,39,38,37,36,
    45,41,37,33,43,42,41,40,
    44,40,36,32,47,46,45,44
])

ARRANGE_MASK = torch.tensor([
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
])

class AutoEncoderDataModule(pl.LightningDataModule):
    def __init__(self, data_dir, num_workers=8) -> None:
        super().__init__()
        self.data_dir = data_dir
        self.num_workers = num_workers
        self.calq_cols = [f"CALQ_{i}" for i in range(48)]
        self.norm_data = None
        self.max_data = None
        self.sum_data = None
        self.valid_split = 0.2
        self.val_max = None
        self.val_sum = None

        self.prepare_data()

    @staticmethod
    def add_argparse_args(parent_parser):
        parser = parent_parser.add_argument_group("Dataset")
        parser.add_argument("--data_dir", type=str)
        parser.add_argument("--num_workers", type=int, default=8)
        return parent_parser

    def mask_data(self, data):
        """
        Mask rows where occupancy is zero
        """
        return data[data[self.calq_cols].sum(axis=1) != 0]

    def load_data(self):
        """
        Read and concat all csv files in the data directory into a single
        dataframe
        """
        print(f"Reading files {os.listdir(self.data_dir)}")
        data = pd.concat(
            [
                pd.read_csv(os.path.join(self.data_dir, file))
                for file in os.listdir(self.data_dir)
            ]
        )
        data = self.mask_data(data)
        data = data[self.calq_cols].astype("float64")
        # data.to_pickle(os.path.join(self.data_dir, "data.pkl"))
        print(f"Input data shape: {data.shape}")

        return data.values

    def prep_input(self, norm_data, shape=(1, 8, 8)):
        """
        Prepare the input data for the model
        """
        input_data = norm_data[:, ARRANGE]
        input_data[:, ARRANGE_MASK == 0] = 0 # zero out repeated entries
        shaped_data = input_data.reshape(len(input_data), shape[0], shape[1], shape[2])
        print(f"Prepped shaped data shape: {shaped_data.shape}")
        return shaped_data

    def prepare_data(self):
        data = self.load_data()
        self.norm_data, self.max_data, self.sum_data = normalize(data.copy())
        self.max_data = self.max_data / 35.0  # normalize to units of transverse MIPs
        self.sum_data = self.sum_data / 35.0  # normalize to units of transverse MIPs
        self.shaped_data = self.prep_input(self.norm_data)

    def train_dataloader(self):
        """
        Return the training dataloader
        """
        train_data = self.shaped_data[
            int(len(self.shaped_data) * self.valid_split) :
        ]

        return torch.utils.data.DataLoader(
            train_data, batch_size=500, shuffle=True, num_workers=self.num_workers
        )

    def val_dataloader(self):
        """
        Return the validation dataloader
        """
        # Take the first valid_split% of the data as validation data
        val_data = self.shaped_data[
            : int(len(self.shaped_data) * self.valid_split)
        ]
        val_index = np.arange(int(len(self.shaped_data) * self.valid_split))
        self.val_max = self.max_data[val_index]
        self.val_sum = self.sum_data[val_index]

        return torch.utils.data.DataLoader(
            val_data, batch_size=500, shuffle=False, num_workers=self.num_workers
        )

    def test_dataloader(self):
        """
        Return the test dataloader
        """
        return self.val_dataloader()

    def get_val_max(self):
        return self.val_max
    
    def get_val_sum(self):
        return self.val_sum
