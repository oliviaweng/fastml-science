# *
# @file Different utility functions
# Copyright (c) Zhewei Yao, Amir Gholami
# All rights reserved.
# This file is part of PyHessian library.
#
# PyHessian is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyHessian is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyHessian.  If not, see <http://www.gnu.org/licenses/>.
# *

from __future__ import print_function

import os
import numpy as np
import argparse
import torch
import pandas as pd
import matplotlib.pyplot as plt

# from density_plot import get_esd_plot
from pyhessian import hessian
from autoencoder_datamodule import AutoEncoderDataModule
from autoencoder import AutoEncoder
from autoencoder_trainer import test_model


##
import matplotlib as mpl

mpl.rcParams["axes.prop_cycle"] = mpl.cycler(
    color=[
        "#DB4437",
        "#4285F4",
        "#F4B400",
        "#0F9D58",
        "purple",
        "goldenrod",
        "peru",
        "coral",
        "turquoise",
        "gray",
        "navy",
        "m",
        "darkgreen",
        "fuchsia",
        "steelblue",
    ]
)
cols = [
    "#DB4437",
    "#4285F4",
    "#F4B400",
    "#0F9D58",
    "purple",
    "goldenrod",
    "peru",
    "coral",
    "turquoise",
    "gray",
    "navy",
    "m",
    "darkgreen",
    "fuchsia",
    "steelblue",
]
# from autoencoder_classes import AE,VAE
import mplhep as hep

hep.style.use("CMS")
# hep.style.use(hep.style.ROOT)


def main(args):
    # set random seed to reproduce the work
    torch.manual_seed(args.seed)
    if args.cuda:
        torch.cuda.manual_seed(args.seed)

    for arg in vars(args):
        print(arg, getattr(args, arg))

    data_module = AutoEncoderDataModule.from_argparse_args(args)
    data_module.setup("")
    args.mini_hessian_batch_size = args.batch_size
    ##############
    # Get the hessian data
    ##############
    assert args.hessian_batch_size % args.mini_hessian_batch_size == 0
    assert 50000 % args.hessian_batch_size == 0
    batch_num = args.hessian_batch_size // args.mini_hessian_batch_size

    if batch_num == 1:
        for inputs in data_module.val_dataloader():
            hessian_dataloader = (inputs, inputs)
            break
    else:
        hessian_dataloader = []
        for i, inputs in enumerate(data_module.val_dataloader()):
            hessian_dataloader.append((inputs, inputs))
            if i == batch_num - 1:
                break

    # get model
    model = AutoEncoder.load_from_checkpoint(args.checkpoint)

    if args.cuda:
        model = model.cuda()
        print("Moved model to GPU")

    criterion = model.loss  # telescopeMSE8x8 Loss
    # criterion = nn.BCELoss()

    ###################
    # Get model checkpoint, get saving folder
    ###################
    if args.checkpoint == "":
        raise Exception("please choose the trained model")


    # Compute EMD
    # Need val_sum to compute EMD
    # _, val_sum = data_module.get_val_max_and_sum()
    # model.set_val_sum(val_sum)
    # data_module.setup("test")
    # _ = test_model(model, data_module.test_dataloader())

    ######################################################
    # Begin the computation
    ######################################################
    # layers = ["conv", "enc_dense", "dec_dense", "convtrans2d1", "convtrans2d2"]  # Autoencoder
    # layers = ["dense_1","dense_2","dense_3","dense_4"]  # jettagger

    # turn model to eval mode
    model.eval()
    if batch_num == 1:
        hessian_comp = hessian(
            model,
            criterion,
            # layers,
            data=hessian_dataloader,
            cuda=args.cuda,
        )
    else:
        hessian_comp = hessian(
            model,
            criterion,
            # layers,
            dataloader=hessian_dataloader,
            cuda=args.cuda,
        )


    print("********** finish data loading and begin Hessian computation **********")

    (
        top_eigenvalues,
        top_eigenvector,
        eigenvalueL,
        eigenvectorL,
    ) = hessian_comp.eigenvalues(top_n=1)
    trace, traceL = hessian_comp.trace()
    # density_eigen, density_weight = hessian_comp.density()


    log_dict = {}
    log_dict["model"] = args.model_tag
    mean_traces = []
    for trace_vhv in traceL:
        mean_trace = np.mean(traceL[trace_vhv])
        mean_traces.append(mean_trace)
        log_dict[f"mean_trace_{trace_vhv}"] = [mean_trace]
    
    print("\n***Top Eigenvalues per Layer: ", eigenvalueL)
    for layer in eigenvectorL:
        print("\n***Top Eigenvectors per Layer: ", layer)
        for top_eigenvs in eigenvectorL[layer]:
            for eigen_v in top_eigenvs:
                print("\n***eigenvector shape = ", eigen_v.shape)
    print("\n***Avg Trace: ", np.mean(trace))
    # print("\n***Avg Eigenvalue density: ", np.mean(density_eigen))
    # print("\n***Avg Weight Density: ", np.mean(density_weight))

    print("##############################################")
    print(mean_traces)
    print("##############################################")

    log_df = pd.DataFrame(data=log_dict)
    write_mode = "a" if os.path.exists(args.logfile) else "w"
    log_df.to_csv(
        args.logfile, mode=write_mode, index=False, header=not os.path.exists(args.logfile)
    )


    plt.figure(figsize=(18, 12))
    plt.plot(mean_traces, "o-")
    plt.xlabel("Layers")
    plt.ylabel("Average Hessian Trace")
    plt.xticks(list(range(len(traceL))), traceL)
    plt.grid()
    plt.legend()
    plt.savefig(f"plots/{args.model_tag}-autoencoder-trace.pdf")
    plt.yscale("log")
    plt.savefig(f"plots/{args.model_tag}-autoencoder-trace-log.pdf")
    plt.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyTorch Autoencoder")
    parser.add_argument(
        "--mini-hessian-batch-size",
        type=int,
        default=100000,
        help="input batch size for mini-hessian batch (default: 200)",
    )
    parser.add_argument(
        "--hessian-batch-size",
        type=int,
        default=5000,
        help="input batch size for hessian (default: 200)",
    )
    parser.add_argument("--seed", type=int, default=1, help="random seed (default: 1)")
    parser.add_argument("--cuda", action="store_true", default=False, help="Use GPU")
    parser.add_argument("--checkpoint", type=str, default="", help="get the checkpoint")
    parser.add_argument("--model-tag", type=str, default="", help="model tag")
    parser.add_argument("--logfile", type=str, default="logs/hessian.csv", help="log file")
    # Add dataset-specific args
    parser = AutoEncoderDataModule.add_argparse_args(parser)
    args = parser.parse_args()
    main(args)
