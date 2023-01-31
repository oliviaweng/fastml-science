import os
import torch
import numpy as np
import pandas as pd
import pytorch_lightning as pl


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

    def mask_data(self, data):
        """
        Mask rows where occupancy is zero
        """
        return data[data[self.calq_cols].sum(axis=1) != 0]

    def normalize(self, data, sumlog2=True):
        """
        Normalize data by dividing by the sum of the log2 of the occupancy
        """
        maxes = []
        sums = []
        sums_log2 = []
        for i in range(len(data)):
            maxes.append(data[i].max())
            sums.append(data[i].sum())
            sums_log2.append(2 ** (np.floor(np.log2(data[i].sum()))))
            if sumlog2:
                data[i] = 1.0 * data[i] / (sums_log2[-1] if sums_log2[-1] else 1.0)
            else:
                data[i] = 1.0 * data[i] / (data[i].sum() if data[i].sum() else 1.0)
        sums_arr = np.array(sums_log2) if sumlog2 else np.array(sums)
        return (
            data,
            np.array(maxes),
            sums_arr,
        )

    def unnormalize(self, norm_data, max_vals, sumlog2=True):
        for i in range(len(norm_data)):
            if sumlog2:
                sumlog2 = 2 ** (np.floor(np.log2(norm_data[i].sum())))
                norm_data[i] = (
                    norm_data[i] * max_vals[i] / (sumlog2 if sumlog2 else 1.0)
                )
            else:
                norm_data[i] = (
                    norm_data[i]
                    * max_vals[i]
                    / (norm_data[i].sum() if norm_data[i].sum() else 1.0)
                )
        return norm_data

    def load_data(self):
        """
        Read and concat all csv files in the data directory into a single
        dataframe and save it as a pickle file
        """
        data = pd.concat(
            [
                pd.read_csv(os.path.join(self.data_dir, file))
                for file in os.listdir(self.data_dir)
            ]
        )
        data = self.mask_data(data)
        data = data[self.calq_cols].astype("float64")
        data.to_pickle(os.path.join(self.data_dir, "data.pkl"))
        print(f"Input data shape: {data.shape}")

        return data.values

    def prep_input(self, norm_data, shape=(4, 4, 3)):
        """
        Prepare the input data for the model
        """
        shaped_data = norm_data.reshape(len(norm_data), shape[0], shape[1], shape[2])
        return shaped_data

    def prepare_data(self):
        data = self.load_data()
        self.norm_data, self.max_data, self.sum_data = self.normalize(data.copy())
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

    # TODO: Add getter methods for val_max and val_sum