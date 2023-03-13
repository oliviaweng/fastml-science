import os
import argparse
import numpy as np
from pathlib import Path

from qDenseCNN import qDenseCNN
from denseCNN import denseCNN

from fkeras.fmodel import FModel
from fkeras.metrics.hessian import HessianMetrics
from telescope import telescopeMSE8x8_for_FKeras

from tensorflow.keras.models import Model

import tensorflow as tf

import time

from utils.metrics import emd_multiproc
from train import (
    load_data,
    normalize,
    build_model,
    split,
    train,
    evaluate_model,
    evaluate_model_experiment,
    unnormalize,
)

from decimal import Decimal

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

def pre_exit_procedure(open_files):
    print("[pre_exit_procedure] Manual exit initiated. Closing open experiment files.")
    for f in open_files:
        f.write("[pre_exit_procedure] Manual exit initiated. Closing this file.")
        f.close()
    exit()

def exp_file_write(file_path, input_str, open_mode="a"):
    with open(file_path, open_mode) as f:
        f.write(input_str)

def main(args):
    #S: Running eagerly is essential. Without eager execution mode,
    ### the fkeras.utils functions (e.g., gen_mask_tensor) only get
    ### get evaluated once and then subsequent "calls" reuse the 
    ### same value from the initial call (which manifest as the
    ### same fault(s) being injected over and over again)
    tf.config.run_functions_eagerly(True)
    # tf.data.experimental.enable_debug_mode()

    efd_fp = args.efd_fp #"./efd_val_inputs_0-31_with_eager_exec_cleaning.log"
    efr_fp = args.efr_fp #"./efr_val_inputs_0-31_with_eager_exec_cleaning.log"
    if args.efx_overwrite:
        exp_file_write(efd_fp, "", "w")
        exp_file_write(efr_fp, "", "w")   
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
    model_info["m_autoCNN"] = m_autoCNN
    model_info["m_autoCNNen"] = m_autoCNNen

    val_max = maxdata[val_ind]
    val_sum = sumdata[val_ind]

    if model_info["ws"] == "":
        raise RuntimeError("No weights provided to preload into the model!")
    
    #S: Instantiate the FKeras model to be used
    fmodel = FModel(m_autoCNNen, 0.0)
    print(fmodel.layer_bit_ranges)

    #S: Configure how many validation inputs will be used
    curr_val_input = val_input
    if 0 < args.num_val_inputs < val_input.shape[0]:
        curr_val_input = val_input[:args.num_val_inputs]
    else:
        raise RuntimeError("Improper configuration for 'num_val_inputs'")

    #S: Configure which bits will be flipped
    # bit_flip_range_step = (0,2, 1)
    bit_flip_range_step = (0,fmodel.num_model_param_bits, 1)
    if (args.use_custom_bfr == 1): 
        bfr_start_ok = (0 <= args.bfr_start) and (args.bfr_start<= fmodel.num_model_param_bits)
        bfr_end_ok   = (0 <= args.bfr_end  ) and (args.bfr_end  <= fmodel.num_model_param_bits)
        bfr_ok = bfr_start_ok and bfr_end_ok
        if bfr_ok:
            bit_flip_range_step = (args.bfr_start, args.bfr_end, args.bfr_step)
        else:
            raise RuntimeError("Improper configuration for bit flipping range")

    #S: Begin the single fault injection (bit flipping) campaign
    for bit_i in range(*bit_flip_range_step):

        #S: Flip the desired bit in the model 
        fmodel.explicit_select_model_param_bitflip([bit_i])

        model.encoder = fmodel.model

        f_autoencoder = Model(
            model.inputs, model.decoder(fmodel.model(model.inputs)), name="autoencoder"
        )
        model.autoencoder = f_autoencoder
        model_info["m_autoCNN"] = f_autoencoder
        model_info["m_autoCNNen"] = fmodel.model

        cnn_enQ = fmodel.model.predict(curr_val_input)
        cnn_deQ = model.decoder.predict(cnn_enQ)
        cnn_enQ = np.reshape(cnn_enQ, (len(cnn_enQ), model.pams["encoded_dim"], 1))
        input_Q = curr_val_input

        #I: Useful for debugging
        #exp_file_write(efd_fp, f"Eval Only: {args.evalOnly}\n")
        #exp_file_write(efd_fp, f"'val_input' type : {type(val_input)}\n")
        #exp_file_write(efd_fp, f"'val_input' shape: {val_input.shape}\n")
        #exp_file_write(efd_fp, f"'cnn_enQ' type : {type(cnn_enQ)}\n")
        #exp_file_write(efd_fp, f"'cnn_enQ' shape: {cnn_enQ.shape}\n")
        #pre_exit_procedure([exp_file_debug, exp_file_result])

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

        #S: Evaluate the model and write results to result file 
        emd_vals = evaluate_model_experiment(model_info, charges, aux_arrs, eval_dict, args, [efd_fp, efr_fp])

        #######################
        # New Code START
        #######################
        hess_start = time.time()
        hess = HessianMetrics(f_autoencoder, telescopeMSE8x8_for_FKeras, curr_val_input, curr_val_input)
        hess_trace_dict = hess.trace_hack(max_iter=500)
        exp_file_write(efd_fp, f'Hessian trace compute time: {time.time() - hess_start} seconds\n')
        exp_file_write(efd_fp,  "hess_trace_dict = {\n")
        for k, v in hess_trace_dict.items():
            exp_file_write(efd_fp,f"\t'{k}':{v},\n")
        exp_file_write(efd_fp, "}\n\n")
        #######################
        # New Code END
        #######################
        
        exp_file_write(efr_fp, f"(val_i, bit_i) | emd_val | hess_trace_dict\n")
        for val_i, val in enumerate(emd_vals):
            exp_file_write(efr_fp, f"({val_i},{bit_i}) | {Decimal.from_float(val)} | {hess_trace_dict}\n")
        
        #I: Useful for debugging
        # for fmodel_layer in fmodel.model.layers:
        #     if fmodel_layer.__class__.__name__ in ["FQDense", "FQConv2D"]:
        #         print(f"Model flbrs = {fmodel_layer.flbrs}")


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

    # args.bfr_start, args.bfr_end, args.bfr_step
    args = parser.parse_args()
    main(args)


# import os
# import argparse
# import numpy as np
# from pathlib import Path

# from qDenseCNN import qDenseCNN
# from denseCNN import denseCNN

# from fkeras.fmodel import FModel
# from tensorflow.keras.models import Model

# import tensorflow as tf

# from utils.metrics import emd_multiproc
# from train import (
#     load_data,
#     normalize,
#     build_model,
#     split,
#     train,
#     evaluate_model,
#     evaluate_model_experiment,
#     unnormalize,
# )

# from decimal import Decimal

# def normalize_data(data_values):
#     # normalize input charge data rescaleInputToMax: normalizes charges to
#     # maximum charge in module sumlog2 (default): normalizes charges to
#     # 2**floor(log2(sum of charge in module)) where floor is the largest scalar
#     # integer: i.e. normalizes to MSB of the sum of charges (MSB here is the
#     # most significant bit) rescaleSum: normalizes charges to sum of charge in
#     # module
#     norm_data, max_data, sum_data = normalize(
#         data_values.copy(), rescaleInputToMax=args.rescaleInputToMax, sumlog2=True
#     )

#     return norm_data, max_data, sum_data


# def model_setup(model_info, output_dir):
#     model_name = model_info["name"]
#     model_output_dir = os.path.join(output_dir, model_name)
#     if not os.path.exists(model_output_dir):
#         os.mkdir(model_output_dir)

#     if model_info["isQK"]:
#         print("Model is a qDenseCNN")
#         m = qDenseCNN(weights_f=model_info["ws"])
#     else:
#         print.info("Model is a denseCNN")
#         m = denseCNN(weights_f=model_info["ws"])
#     m.setpams(model_info["params"])
#     m.init()

#     return m

# def pre_exit_procedure(open_files):
#     print("[pre_exit_procedure] Manual exit initiated. Closing open experiment files.")
#     for f in open_files:
#         f.write("[pre_exit_procedure] Manual exit initiated. Closing this file.")
#         f.close()
#     exit()

# def exp_file_write(file_path, input_str, open_mode="a"):
#     with open(file_path, open_mode) as f:
#         f.write(input_str)

# def main(args):
#     #S: Running eagerly is essential. Without eager execution mode,
#     ### the fkeras.utils functions (e.g., gen_mask_tensor) only get
#     ### get evaluated once and then subsequent "calls" reuse the 
#     ### same value from the initial call (which manifest as the
#     ### same fault(s) being injected over and over again)
#     tf.config.run_functions_eagerly(True)
#     # tf.data.experimental.enable_debug_mode()

#     efd_fp = args.efd_fp #"./efd_val_inputs_0-31_with_eager_exec_cleaning.log"
#     efr_fp = args.efr_fp #"./efr_val_inputs_0-31_with_eager_exec_cleaning.log"
#     if args.efx_overwrite:
#         exp_file_write(efd_fp, "", "w")
#         exp_file_write(efr_fp, "", "w")   
#     print(args)
#     if "nElinks_%s" % args.nElinks not in args.inputFile:
#         raise RuntimeError(
#             f"nElinks={args.nElinks} while 'nElinks_{args.nElinks}' isn't in '{args.inputFile}', this will cause wrong BC and STC settings"
#         )

#     # load data
#     data_values, phys_values = load_data(args)
#     normdata, maxdata, sumdata = normalize_data(data_values)
#     maxdata = maxdata / 35.0  # normalize to units of transverse MIPs
#     sumdata = sumdata / 35.0  # normalize to units of transverse MIPs

#     # Returns a list of models, but we will only ever test one model at a time
#     model_info = build_model(args)[0]

#     eval_dict = {
#         # compare to other algorithms
#         "algnames": ["ae", "stc", "thr_lo", "thr_hi", "bc"],
#         "metrics": {"EMD": emd_multiproc},
#         "occ_nbins": 12,
#         "occ_range": (0, 24),
#         "occ_bins": [0, 2, 5, 10, 15],
#         "chg_nbins": 20,
#         "chg_range": (0, 200),
#         "chglog_nbins": 20,
#         "chglog_range": (0, 2.5),
#         "chg_bins": [0, 2, 5, 10, 50],
#         "occTitle": r"occupancy [1 MIP$_{\mathrm{T}}$ TCs]",
#         "logMaxTitle": r"log10(Max TC charge/MIP$_{\mathrm{T}}$)",
#         "logTotTitle": r"log10(Sum of TC charges/MIP$_{\mathrm{T}}$)",
#     }

#     if not os.path.exists(args.odir):
#         os.makedirs(args.odir)

#     # performance dictionary
#     perf_dict = {}

#     # Putting back physics columns below once training is done
#     Nphys = round(len(phys_values) * 0.2)
#     phys_val_input = phys_values[:Nphys]

#     # Model setup
#     model = model_setup(model_info, args.odir)

#     # split in training/validation datasets
#     shaped_data = model.prepInput(normdata)
#     if args.evalOnly:
#         print("Eval only")
#         val_input = shaped_data
#         val_ind = np.array(range(len(shaped_data)))
#         train_input = val_input[:0]  # empty with correct shape
#         train_ind = val_ind[:0]
#     else:
#         val_input, train_input, val_ind, train_ind = split(shaped_data)

#     m_autoCNN, m_autoCNNen = model.get_models()
#     model_info["m_autoCNN"] = m_autoCNN
#     model_info["m_autoCNNen"] = m_autoCNNen

#     val_max = maxdata[val_ind]
#     val_sum = sumdata[val_ind]

#     if model_info["ws"] == "":
#         raise RuntimeError("No weights provided to preload into the model!")
    
#     #S: Instantiate the FKeras model to be used
#     fmodel = FModel(m_autoCNNen, 0.0)
#     print(fmodel.layer_bit_ranges)

#     #S: Configure how many validation inputs will be used
#     curr_val_input = val_input
#     if 0 < args.num_val_inputs < val_input.shape[0]:
#         curr_val_input = val_input[:args.num_val_inputs]
#     else:
#         raise RuntimeError("Improper configuration for 'num_val_inputs'")

#     #S: Configure which bits will be flipped
#     # bit_flip_range_step = (0,2, 1)
#     bit_flip_range_step = (0,fmodel.num_model_param_bits, 1)
#     if (args.use_custom_bfr == 1): 
#         bfr_start_ok = (0 <= args.bfr_start) and (args.bfr_start<= fmodel.num_model_param_bits)
#         bfr_end_ok   = (0 <= args.bfr_end  ) and (args.bfr_end  <= fmodel.num_model_param_bits)
#         bfr_ok = bfr_start_ok and bfr_end_ok
#         if bfr_ok:
#             bit_flip_range_step = (args.bfr_start, args.bfr_end, args.bfr_step)
#         else:
#             raise RuntimeError("Improper configuration for bit flipping range")

#     #S: Begin the single fault injection (bit flipping) campaign
#     for bit_i in range(*bit_flip_range_step):

#         #S: Flip the desired bit in the model 
#         fmodel.explicit_select_model_param_bitflip([bit_i])

#         model.encoder = fmodel.model

#         f_autoencoder = Model(
#             model.inputs, model.decoder(fmodel.model(model.inputs)), name="autoencoder"
#         )
#         model.autoencoder = f_autoencoder
#         model_info["m_autoCNN"] = f_autoencoder
#         model_info["m_autoCNNen"] = fmodel.model

#         cnn_enQ = fmodel.model.predict(curr_val_input)
#         cnn_deQ = model.decoder.predict(cnn_enQ)
#         cnn_enQ = np.reshape(cnn_enQ, (len(cnn_enQ), model.pams["encoded_dim"], 1))
#         input_Q = curr_val_input

#         #I: Useful for debugging
#         #exp_file_write(efd_fp, f"Eval Only: {args.evalOnly}\n")
#         #exp_file_write(efd_fp, f"'val_input' type : {type(val_input)}\n")
#         #exp_file_write(efd_fp, f"'val_input' shape: {val_input.shape}\n")
#         #exp_file_write(efd_fp, f"'cnn_enQ' type : {type(cnn_enQ)}\n")
#         #exp_file_write(efd_fp, f"'cnn_enQ' shape: {cnn_enQ.shape}\n")
#         #pre_exit_procedure([exp_file_debug, exp_file_result])

#         input_calQ = model.mapToCalQ(input_Q)  # shape = (N,48) in CALQ order
#         output_calQ_fr = model.mapToCalQ(cnn_deQ)  # shape = (N,48) in CALQ order

#         print("Restore normalization")
#         input_Q_abs = (
#             np.array(
#                 [
#                     input_Q[i] * (val_max[i] if args.rescaleInputToMax else val_sum[i])
#                     for i in range(0, len(input_Q))
#                 ]
#             )
#             * 35.0
#         )  # restore abs input in CALQ unit
#         input_calQ = np.array(
#             [
#                 input_calQ[i] * (val_max[i] if args.rescaleInputToMax else val_sum[i])
#                 for i in range(0, len(input_calQ))
#             ]
#         )  # shape = (N,48) in CALQ order
#         output_calQ = unnormalize(
#             output_calQ_fr.copy(),
#             val_max if args.rescaleOutputToMax else val_sum,
#             rescaleOutputToMax=args.rescaleOutputToMax,
#         )

#         occupancy_1MT = np.count_nonzero(input_calQ.reshape(len(input_Q), 48) > 1.0, axis=1)

#         eval_dict = {
#             # compare to other algorithms
#             "algnames": ["ae", "stc", "thr_lo", "thr_hi", "bc"],
#             # 'metrics'     :{'EMD': emd},
#             "metrics": {"EMD": emd_multiproc},
#             "occ_nbins": 12,
#             "occ_range": (0, 24),
#             "occ_bins": [0, 2, 5, 10, 15],
#             "chg_nbins": 20,
#             "chg_range": (0, 200),
#             "chglog_nbins": 20,
#             "chglog_range": (0, 2.5),
#             "chg_bins": [0, 2, 5, 10, 50],
#             "occTitle": r"occupancy [1 MIP$_{\mathrm{T}}$ TCs]",
#             "logMaxTitle": r"log10(Max TC charge/MIP$_{\mathrm{T}}$)",
#             "logTotTitle": r"log10(Sum of TC charges/MIP$_{\mathrm{T}}$)",
#         }

#         charges = {
#             "input_Q": input_Q,
#             "input_Q_abs": input_Q_abs,
#             "input_calQ": input_calQ,  # shape = (N,48) (in abs Q)   (in CALQ 1-48 order)
#             "output_calQ": output_calQ,  # shape = (N,48) (in abs Q)   (in CALQ 1-48 order)
#             "output_calQ_fr": output_calQ_fr,  # shape = (N,48) (in Q fr)   (in CALQ 1-48 order)
#             "cnn_deQ": cnn_deQ,
#             "cnn_enQ": cnn_enQ,
#             "val_sum": val_sum,
#             "val_max": val_max,
#         }

#         aux_arrs = {"occupancy_1MT": occupancy_1MT}

        
#         #S: Evaluate the model and write results to result file 
#         emd_vals = evaluate_model_experiment(model_info, charges, aux_arrs, eval_dict, args, [efd_fp, efr_fp])
#         exp_file_write(efr_fp, f"(val_i, bit_i) | emd_val\n")
#         for val_i, val in enumerate(emd_vals):
#             exp_file_write(efr_fp, f"({val_i},{bit_i}) | {Decimal.from_float(val)}\n")
        
#         #I: Useful for debugging
#         # for fmodel_layer in fmodel.model.layers:
#         #     if fmodel_layer.__class__.__name__ in ["FQDense", "FQConv2D"]:
#         #         print(f"Model flbrs = {fmodel_layer.flbrs}")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()

#     parser.add_argument(
#         "-i",
#         "--inputFile",
#         type=str,
#         default="data/nElinks_5/",
#         dest="inputFile",
#         help="input TSG files",
#     )
#     parser.add_argument(
#         "-o",
#         "--odir",
#         type=str,
#         default="output/",
#         dest="odir",
#         help="output directory",
#     )
#     parser.add_argument(
#         "--epochs",
#         type=int,
#         default=200,
#         dest="epochs",
#         help="number of epochs to train",
#     )
#     parser.add_argument(
#         "--nELinks",
#         type=int,
#         default=5,
#         dest="nElinks",
#         help="n of active transceiver e-links eTX",
#     )
#     parser.add_argument(
#         "--evalOnly",
#         action="store_true",
#         default=False,
#         dest="evalOnly",
#         help="only evaluate the NN on the input sample, no train",
#     )
#     parser.add_argument(
#         "--AEonly", type=int, default=1, dest="AEonly", help="run only AE algo"
#     )
#     parser.add_argument(
#         "--nrowsPerFile",
#         type=int,
#         default=5000000,
#         dest="nrowsPerFile",
#         help="load nrowsPerFile in a directory",
#     )
#     parser.add_argument(
#         "--noHeader",
#         action="store_true",
#         default=False,
#         dest="noHeader",
#         help="input data has no header",
#     )
#     parser.add_argument(
#         "--rescaleInputToMax",
#         action="store_true",
#         default=False,
#         dest="rescaleInputToMax",
#         help="rescale the input images so the maximum deposit is 1. Else normalize",
#     )
#     parser.add_argument(
#         "--rescaleOutputToMax",
#         action="store_true",
#         default=False,
#         dest="rescaleOutputToMax",
#         help="rescale the output images to match the initial sum of charge",
#     )
#     parser.add_argument(
#         "--maskPartials",
#         action="store_true",
#         default=False,
#         dest="maskPartials",
#         help="mask partial modules",
#     )
#     parser.add_argument(
#         "--maskEnergies",
#         action="store_true",
#         default=False,
#         dest="maskEnergies",
#         help="Mask energy fractions <= 0.05",
#     )
#     parser.add_argument(
#         "--saveEnergy",
#         action="store_true",
#         default=False,
#         dest="saveEnergy",
#         help="save SimEnergy from input data",
#     )
#     parser.add_argument(
#         "--double",
#         action="store_true",
#         default=False,
#         dest="double",
#         help="test PU400 by combining PU200 events",
#     )
#     parser.add_argument(
#         "--skipPlot",
#         action="store_true",
#         default=False,
#         dest="skipPlot",
#         help="skip the plotting step",
#     )
#     parser.add_argument(
#         "--loss", type=str, default=None, dest="loss", help="force loss function to use"
#     )
#     parser.add_argument(
#         "--models",
#         type=str,
#         default="8x8_c8_S2_tele",
#         dest="models",
#         help="models to run, if empty string run all",
#     )
#     parser.add_argument(
#         "--pretrained-model",
#         type=str,
#         default="",
#         help="path to pretrained model .hdf5 file",
#     )
#     parser.add_argument(
#         "--eval-ber",
#         type=float,
#         default=0,
#         help="Bit error rate of the whole model during model evaluation",
#     )
#     parser.add_argument(
#         "--log-file", type=Path, default="log.txt", help="path to log file"
#     )
    
#     #I: Arguments for bit flipping experiment
#     parser.add_argument(
#         "--efd_fp",
#         type=str,
#         default="./efd.log",
#         help="File path for experiment file with debugging data",
#     )
#     parser.add_argument(
#         "--efr_fp",
#         type=str,
#         default="./efr.log",
#         help="File path for experiment file with result data",
#     )
#     parser.add_argument(
#         "--efx_overwrite",
#         type=int,
#         default=0,
#         help="If '0', efd_fp and efr_fp are appended to with data; If '1', efd_fp and efr_fp are overwritten with data",
#     )
#     parser.add_argument(
#         "--use_custom_bfr",
#         type=int,
#         default=0,
#         help="If '0', all bits (of supported layers) will be flipped. If '1', all bits in the range (--bfr_start, --bfr_end, --bfr_step) will be flipped",
#     )
#     parser.add_argument(
#         "--bfr_start",
#         type=int,
#         default=0,
#         help="Bit flipping range start. Note: bit index starts at 0.",
#     )
#     parser.add_argument(
#         "--bfr_end",
#         type=int,
#         default=2,
#         help="Bit flipping range end (exclusive). Note: bit index starts at 0.",
#     )
#     parser.add_argument(
#         "--bfr_step",
#         type=int,
#         default=1,
#         help="Bit flipping range step size.",
#     )
#     parser.add_argument(
#         "--num_val_inputs",
#         type=int,
#         default=2,
#         help="Number of validation inputs to use for evaluating the faulty models",
#     )

#     # args.bfr_start, args.bfr_end, args.bfr_step
#     args = parser.parse_args()
#     main(args)