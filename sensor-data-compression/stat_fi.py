import os
import time
import json
import argparse
import numpy as np
from pathlib import Path

import tensorflow as tf
from tensorflow.keras.models import Model

from denseCNN import denseCNN
from qDenseCNN import qDenseCNN

import matplotlib
import matplotlib.pyplot as plt

from utils.metrics import emd_multiproc
from train import (
    load_data,
    normalize,
    build_model,
    split,
    evaluate_model,
    unnormalize,
)

from fkeras.fmodel import FModel
from fkeras.metrics.hessian import HessianMetrics
from fkeras.metrics.stat_fi import StatFI
from telescope import telescopeMSE8x8_for_FKeras

# edit depending on where Vivado is installed:
os.environ['PATH'] = '/data/oweng/tools/Xilinx/Vivado/2019.2/bin:' + os.environ['PATH']
# or source settings before running file

# Pickling Utils related imports ##############
import pickle
import codecs

def pickle_object(i_obj, i_output_file_path=None):
    pickled_obj_str = codecs.encode(pickle.dumps(i_obj), "base64").decode()
    
    if i_output_file_path != None:
        with open(i_output_file_path, "w") as f:
            f.write(pickled_obj_str)

    return pickled_obj_str

def unpickle_object_from_str(i_pickle_obj_str):
    return pickle.loads(codecs.decode(i_pickle_obj_str.encode(), "base64"))

def unpickle_object_from_file(i_pickle_file_fp):
    with open(i_pickle_file_fp, "r") as f:
        return unpickle_object_from_str(f.read())
##########################################

"""
Model: "encoder"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 8, 8, 1)]         0         
                                                                 
 input_qa (QActivation)      (None, 8, 8, 1)           0         
                                                                 
 conv2d_0_m (QConv2D)        (None, 4, 4, 8)           80        
                                                                 
 accum1_qa (QActivation)     (None, 4, 4, 8)           0         
                                                                 
 flatten (Flatten)           (None, 128)               0         
                                                                 
 encoded_vector (QDense)     (None, 16)                2064      
                                                                 
 encod_qa (QActivation)      (None, 16)                0         
                                                                 
=================================================================
Total params: 2,144
Trainable params: 2,144
Non-trainable params: 0

"""

def print_dict(d, indent=0):
    align = 20
    for key, value in d.items():
        print('  ' * indent + str(key), end='')
        if isinstance(value, dict):
            print()
            print_dict(value, indent+1)
        else:
            print(':' + ' ' * (20 - len(key) - 2 * indent) + str(value))


def normalize_data(data_values):
    # normalize input charge data rescaleInputToMax: normalizes charges to
    # maximum charge in module sumlog2 (default): normalizes charges to
    # 2**floor(log2(sum of charge in module)) where floor is the largest scalar
    # integer: i.e. normalizes to MSB of the sum of charges (MSB here is the
    # most significant bit) rescaleSum: normalizes charges to sum of charge in
    # module
    norm_data, max_data, sum_data = normalize(
        data_values.copy(), rescaleInputToMax=args.rescaleInputToMax, sumlog2=True
    )

    return norm_data, max_data, sum_data


def model_setup(model_info, output_dir):
    model_name = model_info["name"]
    model_output_dir = os.path.join(output_dir, model_name)
    if not os.path.exists(model_output_dir):
        os.mkdir(model_output_dir)

    if model_info["isQK"]:
        print("Model is a qDenseCNN")
        m = qDenseCNN(weights_f=model_info["ws"])
    else:
        print.info("Model is a denseCNN")
        m = denseCNN(weights_f=model_info["ws"])
    m.setpams(model_info["params"])
    m.init()

    return m


def predict_and_eval_model(model, val_input, val_max, val_sum, args, save_enc_io=False):
    input_Q, cnn_deQ, cnn_enQ = model.predict(val_input)

    if save_enc_io:
        i_file = os.path.join(args.odir, "hgcal_test_input.npy")
        o_file = os.path.join(args.odir, "hgcal_test_output.npy")
        # Save first 10 only
        # np.save(i_file, input_Q[:10])
        # np.save(o_file, cnn_enQ[:10])

        np.save(i_file, input_Q[:2])
        np.save(o_file, cnn_enQ[:2][:, :, 0]) # Remove last dim of 1)

    input_calQ = model.mapToCalQ(input_Q)  # shape = (N,48) in CALQ order
    output_calQ_fr = model.mapToCalQ(cnn_deQ)  # shape = (N,48) in CALQ order

    print("Restore normalization")
    input_Q_abs = (
        np.array(
            [
                input_Q[i] * (val_max[i] if args.rescaleInputToMax else val_sum[i])
                for i in range(0, len(input_Q))
            ]
        )
        * 35.0
    )  # restore abs input in CALQ unit
    input_calQ = np.array(
        [
            input_calQ[i] * (val_max[i] if args.rescaleInputToMax else val_sum[i])
            for i in range(0, len(input_calQ))
        ]
    )  # shape = (N,48) in CALQ order
    output_calQ = unnormalize(
        output_calQ_fr.copy(),
        val_max if args.rescaleOutputToMax else val_sum,
        rescaleOutputToMax=args.rescaleOutputToMax,
    )

    occupancy_1MT = np.count_nonzero(input_calQ.reshape(len(input_Q), 48) > 1.0, axis=1)

    eval_dict = {
        # compare to other algorithms
        "algnames": ["ae", "stc", "thr_lo", "thr_hi", "bc"],
        # 'metrics'     :{'EMD': emd},
        "metrics": {"EMD": emd_multiproc},
        "occ_nbins": 12,
        "occ_range": (0, 24),
        "occ_bins": [0, 2, 5, 10, 15],
        "chg_nbins": 20,
        "chg_range": (0, 200),
        "chglog_nbins": 20,
        "chglog_range": (0, 2.5),
        "chg_bins": [0, 2, 5, 10, 50],
        "occTitle": r"occupancy [1 MIP$_{\mathrm{T}}$ TCs]",
        "logMaxTitle": r"log10(Max TC charge/MIP$_{\mathrm{T}}$)",
        "logTotTitle": r"log10(Sum of TC charges/MIP$_{\mathrm{T}}$)",
    }

    charges = {
        "input_Q": input_Q,
        "input_Q_abs": input_Q_abs,
        "input_calQ": input_calQ,  # shape = (N,48) (in abs Q)   (in CALQ 1-48 order)
        "output_calQ": output_calQ,  # shape = (N,48) (in abs Q)   (in CALQ 1-48 order)
        "output_calQ_fr": output_calQ_fr,  # shape = (N,48) (in Q fr)   (in CALQ 1-48 order)
        "cnn_deQ": cnn_deQ,
        "cnn_enQ": cnn_enQ,
        "val_sum": val_sum,
        "val_max": val_max,
    }

    aux_arrs = {"occupancy_1MT": occupancy_1MT}

    # Validate EMD performance
    evaluate_model(model, charges, aux_arrs, eval_dict, args)


def main(args):
    # Returns a list of models, but we will only ever test one model at a time
    model_info = build_model(args)[0]

    if not os.path.exists(args.odir):
        os.makedirs(args.odir)

    # Model setup
    model = model_setup(model_info, args.odir)

    m_autoCNN, m_autoCNNen = model.get_models()
    model_info["m_autoCNN"] = m_autoCNN
    model_info["m_autoCNNen"] = m_autoCNNen # encoder only

    

    if model_info["ws"] == "":
        raise RuntimeError("No weights provided to preload into the model!")
    

    #S: Instantiate the FKeras model to be used
    # fmodel = FModel(m_autoCNNen, 0.0)
    # print(fmodel.layer_bit_ranges)

    sfi_model = StatFI(m_autoCNNen)
    params_and_quants = sfi_model.get_params_and_quantizers()
    print(f"{params_and_quants[0].shape}")
    print(f"{params_and_quants[1].shape}")

    fp_pickle = os.path.join(args.odir, args.models) 
    pickle_object(params_and_quants, f"{fp_pickle}_params_and_quantizers.pkl")
    print("Success!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--inputFile",
        type=str,
        default="data/nElinks_5/",
        dest="inputFile",
        help="input TSG files",
    )
    parser.add_argument(
        "-o",
        "--odir",
        type=str,
        default="output/",
        dest="odir",
        help="output directory",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=200,
        dest="epochs",
        help="number of epochs to train",
    )
    parser.add_argument(
        "--nELinks",
        type=int,
        default=5,
        dest="nElinks",
        help="n of active transceiver e-links eTX",
    )
    parser.add_argument(
        "--evalOnly",
        action="store_true",
        default=False,
        dest="evalOnly",
        help="only evaluate the NN on the input sample, no train",
    )
    parser.add_argument(
        "--AEonly", type=int, default=1, dest="AEonly", help="run only AE algo"
    )
    parser.add_argument(
        "--nrowsPerFile",
        type=int,
        default=5000000,
        dest="nrowsPerFile",
        help="load nrowsPerFile in a directory",
    )
    parser.add_argument(
        "--noHeader",
        action="store_true",
        default=False,
        dest="noHeader",
        help="input data has no header",
    )
    parser.add_argument(
        "--rescaleInputToMax",
        action="store_true",
        default=False,
        dest="rescaleInputToMax",
        help="rescale the input images so the maximum deposit is 1. Else normalize",
    )
    parser.add_argument(
        "--rescaleOutputToMax",
        action="store_true",
        default=False,
        dest="rescaleOutputToMax",
        help="rescale the output images to match the initial sum of charge",
    )
    parser.add_argument(
        "--maskPartials",
        action="store_true",
        default=False,
        dest="maskPartials",
        help="mask partial modules",
    )
    parser.add_argument(
        "--maskEnergies",
        action="store_true",
        default=False,
        dest="maskEnergies",
        help="Mask energy fractions <= 0.05",
    )
    parser.add_argument(
        "--saveEnergy",
        action="store_true",
        default=False,
        dest="saveEnergy",
        help="save SimEnergy from input data",
    )
    parser.add_argument(
        "--double",
        action="store_true",
        default=False,
        dest="double",
        help="test PU400 by combining PU200 events",
    )
    parser.add_argument(
        "--skipPlot",
        action="store_true",
        default=False,
        dest="skipPlot",
        help="skip the plotting step",
    )
    parser.add_argument(
        "--loss", type=str, default=None, dest="loss", help="force loss function to use"
    )
    parser.add_argument(
        "--models",
        type=str,
        default="8x8_c8_S2_tele",
        dest="models",
        help="models to run, if empty string run all",
    )
    parser.add_argument(
        "--pretrained-model",
        type=str,
        default="",
        help="path to pretrained model .hdf5 file",
    )
    parser.add_argument(
        "--eval-ber",
        type=float,
        default=0,
        help="Bit error rate of the whole model during model evaluation",
    )
    parser.add_argument(
        "--log-file", type=Path, default="log.txt", help="path to log file"
    )
    # hls4ml args
    parser.add_argument(
        "--input_data_tb",
        type=str,
        default="",
        help="path to input data tb file for csim",
    )
    parser.add_argument(
        "--output_data_tb",
        type=str,
        default="",
        help="path to output data tb file for csim",
    )
    
    args = parser.parse_args()
    main(args)
