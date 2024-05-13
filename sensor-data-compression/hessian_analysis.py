import os
import time
import json
import argparse
import numpy as np
from pathlib import Path

from qDenseCNN import qDenseCNN
from denseCNN import denseCNN

from fkeras.metrics.hessian import HessianMetrics
from fkeras.metrics.stat_fi import StatFI
from telescope import telescopeMSE8x8_for_FKeras
from tensorflow.keras.models import Model

from utils.metrics import emd_multiproc
from train import (
    load_data,
    normalize,
    build_model,
    split,
    train,
    evaluate_model,
    unnormalize,
)

import codecs
import pickle

def exp_file_write(file_path, input_str, open_mode="a"):
    with open(file_path, open_mode) as f:
        f.write(input_str)

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


def main(args):
    print(args)
    if "nElinks_%s" % args.nElinks not in args.inputFile:
        raise RuntimeError(
            f"nElinks={args.nElinks} while 'nElinks_{args.nElinks}' isn't in '{args.inputFile}', this will cause wrong BC and STC settings"
        )

    # load data
    data_values, phys_values = load_data(args)
    normdata, maxdata, sumdata = normalize_data(data_values)
    maxdata = maxdata / 35.0  # normalize to units of transverse MIPs
    sumdata = sumdata / 35.0  # normalize to units of transverse MIPs

    # Returns a list of models, but we will only ever test one model at a time
    model_info = build_model(args)[0]

    eval_dict = {
        # compare to other algorithms
        "algnames": ["ae", "stc", "thr_lo", "thr_hi", "bc"],
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

    if not os.path.exists(args.odir):
        os.makedirs(args.odir)

    # performance dictionary
    perf_dict = {}

    # Putting back physics columns below once training is done
    Nphys = round(len(phys_values) * 0.2)
    phys_val_input = phys_values[:Nphys]

    # Model setup
    model = model_setup(model_info, args.odir)

    # split in training/validation datasets
    shaped_data = model.prepInput(normdata)
    if args.evalOnly:
        print("Eval only")
        val_input = shaped_data
        val_ind = np.array(range(len(shaped_data)))
        train_input = val_input[:0]  # empty with correct shape
        train_ind = val_ind[:0]
    else:
        val_input, train_input, val_ind, train_ind = split(shaped_data)

    m_autoCNN, m_autoCNNen = model.get_models()
    model_info["m_autoCNN"] = m_autoCNN # autoencoder
    model_info["m_autoCNNen"] = m_autoCNNen

    val_max = maxdata[val_ind]
    val_sum = sumdata[val_ind]

    if model_info["ws"] == "":
        raise RuntimeError("No weights provided to preload into the model!")
    
    #S: Configure how many validation inputs will be used
    curr_val_input = val_input
    if 0 < args.num_val_inputs < val_input.shape[0]:
        curr_val_input = val_input[:args.num_val_inputs]
        # For debugging
        # curr_val_input = val_input[args.num_val_inputs:args.num_val_inputs+1]
    else:
        raise RuntimeError("Improper configuration for 'num_val_inputs'")

    # Evaluate the model
    print("Computing Hessian Metrics...")
    # hess_start = time.time()
    
    processed_layer_precision_info = None
    if args.layer_precision_info != None:
        processed_layer_precision_info = eval(args.layer_precision_info[1:-1])

    hess = HessianMetrics(
        m_autoCNN, 
        telescopeMSE8x8_for_FKeras, 
        curr_val_input, 
        curr_val_input,
        batch_size=512,
        layer_precision_info=processed_layer_precision_info
    )
    # hess_trace, layer_traces = hess.trace_hack(max_iter=500)
    # trace_time = time.time() - hess_start
    # print(f'Hessian trace: {hess_trace}')
    # print(f"layer traces {layer_traces}")
    # print(f"Hessian trace compute time: {trace_time} seconds\n")

    # exp_file_write(
    #     os.path.join(args.odir, "hessian_trace_debug.txt"), 
    #     f"{args.num_val_inputs}: {hess_trace}\n"
    # )
    # exp_file_write(
    #     os.path.join(args.odir, "hessian_trace_debug.txt"), 
    #     f"layer_traces: {layer_traces}\n"
    # )
    # exp_file_write(
    #     os.path.join(args.odir, "hessian_trace_debug.txt"), 
    #     f"Num val inputs {args.num_val_inputs} compute time: {trace_time}\n"
    # )
        

    hess_start = time.time()
    top_k = 8
    BIT_WIDTH = args.bit_width
    strategy = "sum"
    # Hessian model-wide sensitivity ranking
    eigenvalues, eigenvectors = hess.top_k_eigenvalues_hack(k=top_k, max_iter=500)
    print("Eigenvectors")
    for i in range(len(eigenvalues)):
        print(f"Top {i+1} eigenvalue: {eigenvalues[i]}")
    print(f'Hessian eigenvalue compute time: {time.time() - hess_start} seconds\n')
    # eigenvalues = None
    rank_start_time = time.time()
    param_ranking, param_scores = hess.hessian_ranking_hack(
        eigenvectors, eigenvalues=eigenvalues, k=top_k, strategy=strategy
    )

    sfi_model = StatFI(m_autoCNNen)
    params_and_quants = sfi_model.get_params_and_quantizers()
    # List where param idx indexes into its associated quantizer idx, which
    # we use to index into the list of quantizers
    # Need ([param0_quant_idx, param1_quant_idx], [quant1, quant2]) for mixed precision
    if processed_layer_precision_info is not None:
        param_idx_to_quant_list = []
        quantizers = []
        # Example: [(800,5),(8192,7)]
        param_counter = 0
        for i, num_param_and_bitwidth in enumerate(processed_layer_precision_info):
            num_params = num_param_and_bitwidth[0]
            quantizers.append(params_and_quants[1][i])
            for _ in range(param_counter, param_counter + num_params):
                param_idx_to_quant_list.append(i)
            param_counter += num_params
        quantizer_info = (param_idx_to_quant_list, quantizers)
    else: # else just a single quantizer for uniform precision
        quantizer_info = params_and_quants[1][0]
    # print(quantizer_info)

    pickled_param_ranking_file = os.path.join(args.odir, f"hessian_ranked_params_{args.model_id}.pkl")
    obj = (list(param_ranking), quantizer_info)
    pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    with open(pickled_param_ranking_file, "w") as f:
        f.write(pickled_obj)
    

    # Compute bit ranking
    # bitwise_rank, bitwise_scores = hess.rank_bits(param_scores, 5) # add m = 5 bits (doesn't work; TODO: delete)
    # bitwise_rank = hess.convert_param_ranking_to_msb_bit_ranking(param_ranking, BIT_WIDTH)

    # pickled_ranking_file = os.path.join(args.odir, f"hessian_ranked_model_bits_iccad_2023_{args.model_id}.pkl")
    
    # obj = list(bitwise_rank)
    # pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    # with open(pickled_ranking_file, "w") as f:
    #     f.write(pickled_obj)

    # gradient_rank, _ = hess.gradient_ranking_hack()
    # bitwise_rank = hess.convert_param_ranking_to_msb_bit_ranking(gradient_rank, BIT_WIDTH)
    
    # pickled_ranking_file = os.path.join(args.odir, f"gradient_ranked_model_bits_iccad_2023_{args.model_id}.pkl")
    # obj = list(bitwise_rank)
    # pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    # with open(pickled_ranking_file, "w") as f:
    #     f.write(pickled_obj)



###############################################
# Gradient ranking
#     grad_start = time.time()
#     grad_ranking, gradients = hess.layer_gradient_ranking()
#     for layer in grad_ranking:
#         exp_file_write(
#             os.path.join(args.odir, f"gradient_ranking_layer_{layer}.txt"),
#             f"Gradient ranking for layer {layer} (param idx, rank)\n",
#             open_mode="w"
#         )
#         for i in range(len(grad_ranking[layer])):
#             exp_file_write(
#                 os.path.join(args.odir, f"gradient_ranking_layer_{layer}.txt"),
#                 f"{grad_ranking[layer][i][0]}, {abs(grad_ranking[layer][i][1])}\n"
#             )
#     print(f'Gradient compute time: {time.time() - grad_start} seconds\n')
#     # Compute L2 distance between gradient and Hessian eigenvectors
#     for layer in layer_eigenvectors:
#         print(f"eigenvector shape: {layer_eigenvectors[layer][0][0].shape}")
#         print(f"gradient shape: {gradients[layer].shape}")
#         print(f'Layer {layer} L2 norm(hessian - gradient) = {np.linalg.norm(layer_eigenvectors[layer][0][0] - gradients[layer])}')
 


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
    
    #I: Arguments for bit flipping experiment
    parser.add_argument(
        "--efd_fp",
        type=str,
        default="./efd.log",
        help="File path for experiment file with debugging data",
    )
    parser.add_argument(
        "--efr_fp",
        type=str,
        default="./efr.log",
        help="File path for experiment file with result data",
    )
    parser.add_argument(
        "--efx_overwrite",
        type=int,
        default=0,
        help="If '0', efd_fp and efr_fp are appended to with data; If '1', efd_fp and efr_fp are overwritten with data",
    )
    parser.add_argument(
        "--use_custom_bfr",
        type=int,
        default=0,
        help="If '0', all bits (of supported layers) will be flipped. If '1', all bits in the range (--bfr_start, --bfr_end, --bfr_step) will be flipped",
    )
    parser.add_argument(
        "--bfr_start",
        type=int,
        default=0,
        help="Bit flipping range start. Note: bit index starts at 0.",
    )
    parser.add_argument(
        "--bfr_end",
        type=int,
        default=2,
        help="Bit flipping range end (exclusive). Note: bit index starts at 0.",
    )
    parser.add_argument(
        "--bfr_step",
        type=int,
        default=1,
        help="Bit flipping range step size.",
    )
    parser.add_argument(
        "--num_val_inputs",
        type=int,
        default=2,
        help="Number of validation inputs to use for evaluating the faulty models",
    )
    parser.add_argument(
        "--bit_width",
        type=int,
        help="Bitwidth of the weights (assuming single precision)",
    )
    parser.add_argument(
        "--layer_precision_info",
        type=str,
        default=None,
        help="List of tuples describing precision information for each layer (assuming mixed precision)",
    )
    parser.add_argument(
        "--model_id",
        type=str,
        help="Model ID string for pickling",
    )

    # args.bfr_start, args.bfr_end, args.bfr_step
    args = parser.parse_args()
    main(args)