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

import hls4ml
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

# edit depending on where Vivado is installed:
os.environ['PATH'] = '/data/oweng/tools/Xilinx/Vivado/2019.2/bin:' + os.environ['PATH']
# or source settings before running file


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
        np.save(i_file, input_Q[:10])
        np.save(o_file, cnn_enQ[:10])

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
    # load data
    ld_data_time_s = time.time()
    data_values, phys_values = load_data(args)
    print(f"Time to load data: {time.time() - ld_data_time_s}")

    normdata, maxdata, sumdata = normalize_data(data_values)
    maxdata = maxdata / 35.0  # normalize to units of transverse MIPs
    sumdata = sumdata / 35.0  # normalize to units of transverse MIPs

    # Returns a list of models, but we will only ever test one model at a time
    model_info = build_model(args)[0]

    if not os.path.exists(args.odir):
        os.makedirs(args.odir)

    # Model setup
    model = model_setup(model_info, args.odir)

    # split in training/validation datasets
    shaped_data = model.prepInput(normdata)
    val_input, train_input, val_ind, train_ind = split(shaped_data)

    m_autoCNN, m_autoCNNen = model.get_models()
    model_info["m_autoCNN"] = m_autoCNN
    model_info["m_autoCNNen"] = m_autoCNNen # encoder only
    
    val_max = maxdata[val_ind]
    val_sum = sumdata[val_ind]

    if model_info["ws"] == "":
        raise RuntimeError("No weights provided to preload into the model!")

    # Validate model performance
    # predict_and_eval_model(model, val_input, val_max, val_sum, args, save_enc_io=True)
    
    # Converting encoder ONLY
    encoder = model.encoder
    config = hls4ml.utils.config_from_keras_model(encoder, granularity='name')
    
    # Custom config settings
    # config["Model"]["Strategy"] = "Resource"
    config["LayerName"]["input_1"]["Precision"]["result"] = "fixed<11,4,RND_CONV,SAT>"
    # TODO: Adjust other layers based on profiling/trace
    
    # For debugging
    for layer in config["LayerName"]:
        config["LayerName"][layer]["Trace"] = True 

    print("-----------------------------------")
    print("Configuration")
    print_dict(config)
    print("-----------------------------------")
    hls_model = hls4ml.converters.convert_from_keras_model(
        encoder, 
        hls_config=config, 
        output_dir=os.path.join(args.odir, "hls4ml_prj"),
        input_data_tb=args.input_data_tb,
        output_data_tb=args.output_data_tb,
        part="xc7z020clg400-1", # pynq-z2
        clock_period=5, # ns
        io_type="io_stream",
    )
    hls4ml.utils.plot_model(
        hls_model, 
        show_shapes=True, 
        show_precision=True, 
        to_file=os.path.join(args.odir, "hls4ml_model.pdf"),
    )
    hls_model.compile()


    # Test hls4ml model & keras model equivalence w/tb data
    input_data_tb = np.load(args.input_data_tb)
    output_data_tb = np.load(args.output_data_tb)[:, :, 0] # Remove last dim of 1
    input_test = np.ascontiguousarray(input_data_tb)
    output_hls = hls_model.predict(input_test)

    hls4ml.model.profiling.numerical(
        model=encoder, hls_model=hls_model, X=input_test,
    )

    plt.show()

    
    for i, out_tb in enumerate(output_data_tb):
        print(f"Sample #{i}")
        print(f"output_hls: {output_hls[i]}")
        print(f"output_tb:  {out_tb}")
        print()
    print(np.isclose(output_hls, output_data_tb))
    # assert np.allclose(output_hls, output_data_tb)

    # Build the model
    hls_model.build(
        reset=True,
        csim=False,
        synth=True,
        cosim=True,
        validation=True,
        export=True,
        vsynth=True,
    )
    hls4ml.report.read_vivado_report(os.path.join(args.odir, "hls4ml_prj"))



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
