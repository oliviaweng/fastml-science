import os
import time
from tqdm import tqdm
import torch
import torchinfo
import numpy as np
import multiprocessing
import pytorch_lightning as pl 
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor
from argparse import ArgumentParser
from autoencoder import AutoEncoder
from autoencoder_datamodule import AutoEncoderDataModule
from utils_pt import unnormalize, emd


def test_model(model, test_loader):
    """
    Our own testing loop instead of using the trainer.test() method so that we
    can multithread EMD computation on the CPU
    """
    model.eval()
    input_calQ_list = []
    output_calQ_list = []
    with torch.no_grad():
        for x in tqdm(test_loader):
            x = x.to(model.device)
            output = model(x)
            input_calQ = model.map_to_calq(x)
            output_calQ_fr = model.map_to_calq(output)
            input_calQ = torch.stack([
                input_calQ[i] * model.val_sum[i] 
                for i in range(len(input_calQ))
            ])  # shape = (batch_size, 48)
            output_calQ = unnormalize(
                torch.clone(output_calQ_fr), model.val_sum
            )  # ae_out
            input_calQ_list.append(input_calQ)
            output_calQ_list.append(output_calQ)
    input_calQ = np.concatenate([i_calQ.cpu() for i_calQ in input_calQ_list], axis=0)
    output_calQ = np.concatenate([o_calQ.cpu() for o_calQ in output_calQ_list], axis=0)
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        emd_list = pool.starmap(emd, zip(input_calQ, output_calQ))
    print(f"EMD computation time: {time.time() - start_time} seconds")
    average_emd = np.mean(np.array(emd_list))
    print(f"Average EMD: {average_emd}")
    return average_emd


def print_model_attributes(model, training_mode=True):
    print("Model attributes")
    print("----------------")
    print(f"model.quantize_act = {model.quantize_act}")
    print(f"model.quantize_weight = {model.quantize_weight}")
    print(f"model.quantize_input = {model.quantize_input}")
    print(f"model.act1_bitwidth = {model.act1_bitwidth}")
    print(f"model.act2_bitwidth = {model.act2_bitwidth}")
    print(f"model.qinput_bitwidth = {model.qinput_bitwidth}")
    print(f"model.batchnorm = {model.batchnorm}")
    if training_mode:
        print(f"model.weight_decay = {model.weight_decay}")
        print(f"model.cos_anneal_warm_restarts = {model.cos_anneal_warm_restarts}")
        print(f"model.warm_restart_freq = {model.warm_restart_freq}")
        print(f"model.lr = {model.lr}")
    
    
def main(args):
    pl.seed_everything(args.seed, workers=True)
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    # ------------------------
    # 0 PREPARE DATA
    # ------------------------
    data_module = AutoEncoderDataModule.from_argparse_args(args)
    if args.process_data:
        print("Processing data...")
        data_module.process_data()
    # ------------------------
    # 1 INIT LIGHTNING MODEL
    # ------------------------
    model = AutoEncoder(
        accelerator=args.accelerator, 
        quantize_act=args.quantize_act,
        quantize_weight=args.quantize_weight,
        quantize_input=args.quantize_input,
        act1_bitwidth=args.act1_bitwidth,
        act2_bitwidth=args.act2_bitwidth,
        qinput_bitwidth=args.qinput_bitwidth,
        batchnorm=args.batchnorm,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        cos_anneal_warm_restarts=args.cos_anneal_warm_restarts,
        warm_restart_freq=args.warm_restart_freq,
        dense_only=args.dense_only, 
        num_dense_feat=args.num_dense_feat,
    )

    torchinfo.summary(model, input_size=(1, 1, 8, 8))  # (B, C, H, W)

    tb_logger = pl_loggers.TensorBoardLogger(args.save_dir, name=args.experiment_name)

    # Save top checkpoint based on validation loss
    top1_checkpoint_callback = ModelCheckpoint(
        save_top_k=1,
        save_last=True,
        monitor="val_loss",
        mode="min",
        dirpath=os.path.join(args.save_dir, args.experiment_name),
        filename=f"{args.experiment_name}" "_epoch={epoch:02d}_loss={val_loss:.3f}",
        auto_insert_metric_name=False,
    )

    # Monitor learning rate
    lr_monitor = LearningRateMonitor(logging_interval="epoch")

    # ------------------------
    # 2 INIT TRAINER
    # ------------------------
    if args.accelerator == "gpu":
        devices = 1 # we support single-gpu training only
    else: # training on cpu
        devices = "auto"
    
    trainer = pl.Trainer(
        max_epochs=args.max_epochs,
        accelerator=args.accelerator,
        logger=tb_logger,
        callbacks=[top1_checkpoint_callback, lr_monitor],
        fast_dev_run=args.fast_dev_run,
        deterministic='warn',
        devices=devices, 
    )

    # Sanity check provided checkpoint file exists
    if args.checkpoint:
        if not os.path.exists(args.checkpoint):
            raise ValueError(f"Provided checkpoint file does not exist: {args.checkpoint}")
    # ------------------------
    # 3 TRAIN MODEL
    # ------------------------
    if args.train:
        if args.checkpoint:
            print(f"Preloading weights from checkpoint: {args.checkpoint}")
            model = AutoEncoder.load_from_checkpoint(
                args.checkpoint,
                accelerator=args.accelerator, 
                quantize_act=args.quantize_act,
                quantize_weight=args.quantize_weight,
                quantize_input=args.quantize_input,
                act1_bitwidth=args.act1_bitwidth,
                act2_bitwidth=args.act2_bitwidth,
                qinput_bitwidth=args.qinput_bitwidth,
                batchnorm=args.batchnorm,
                learning_rate=args.learning_rate,
                strict=False, 
                # Not strict to allow addition of BN params into new model
                weight_decay=args.weight_decay,
                cos_anneal_warm_restarts=args.cos_anneal_warm_restarts,
                warm_restart_freq=args.warm_restart_freq,
                dense_only=args.dense_only, 
                num_dense_feat=args.num_dense_feat,
            )
        print_model_attributes(model)
        trainer.fit(model=model, datamodule=data_module)

    # ------------------------
    # 4 EVALUTE MODEL
    # ------------------------
    evaluate_model = False 
    # Load correct model for eval: 
    #   (1) user-provided model
    #   or
    #   (2) early stopping/best model during training run
    if args.evaluate: 
        if args.checkpoint:
            # Evaluate given checkpoint
            evaluate_model = True
            print(f"Evaluating model saved at: {args.checkpoint}")
            model = AutoEncoder.load_from_checkpoint(
                args.checkpoint,
                accelerator=args.accelerator, 
                quantize_act=args.quantize_act,
                quantize_weight=args.quantize_weight,
                quantize_input=args.quantize_input,
                act1_bitwidth=args.act1_bitwidth,
                act2_bitwidth=args.act2_bitwidth,
                qinput_bitwidth=args.qinput_bitwidth,
                batchnorm=args.batchnorm,
                dense_only=args.dense_only, 
                num_dense_feat=args.num_dense_feat,
            )
            print_model_attributes(model, training_mode=False)
        else:
            raise ValueError("No checkpoint provided for evaluation. Provide a path to checkpoint argument, i.e., --checkpoint CHECKPOINT_PATH") 
    elif args.train:
        evaluate_model = True
        print(f"Evaluating best model saved at: {top1_checkpoint_callback.best_model_path}")
        model = AutoEncoder.load_from_checkpoint(
            top1_checkpoint_callback.best_model_path,
            accelerator=args.accelerator, 
            quantize_act=args.quantize_act,
            quantize_weight=args.quantize_weight,
            quantize_input=args.quantize_input,
            act1_bitwidth=args.act1_bitwidth,
            act2_bitwidth=args.act2_bitwidth,
            qinput_bitwidth=args.qinput_bitwidth,
            batchnorm=args.batchnorm,
            dense_only=args.dense_only, 
            num_dense_feat=args.num_dense_feat,
        )
    if evaluate_model:
        # Need val_sum to compute EMD
        _, val_sum = data_module.get_val_max_and_sum()
        model.set_val_sum(val_sum)
        data_module.setup("test")
        test_results = test_model(model, data_module.test_dataloader())
        eval_tag = "_eval" if args.evaluate else ""
        os.makedirs(os.path.join(args.save_dir, args.experiment_name), exist_ok=True)
        test_results_log = os.path.join(
            args.save_dir, 
            args.experiment_name, 
            args.experiment_name + eval_tag + "_emd.txt"
        )
        with open(test_results_log, "w") as f:
            f.write(str(test_results))
            f.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--process_data", action="store_true", default=False)
    parser.add_argument("--max_epochs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--save_dir", type=str, default="./pt_autoencoder_test")
    parser.add_argument("--experiment_name", type=str, default="autoencoder")
    parser.add_argument("--fast_dev_run", action="store_true", default=False)
    parser.add_argument(
        "--accelerator", type=str, choices=["cpu", "gpu", "auto"], default="gpu"
    )
    parser.add_argument("--checkpoint", type=str, default=None, help="model checkpoint")
    parser.add_argument("--train", action="store_true", default=False)
    parser.add_argument("--evaluate", action="store_true", default=False)
    parser.add_argument(
        "--quantize_act", 
        action="store_true", 
        default=False, 
        help="quantize activations"
    )
    parser.add_argument(
        "--quantize_weight", 
        action="store_true", 
        default=False, 
        help="quantize weights"
    )
    parser.add_argument(
        "--quantize_input", 
        action="store_true", 
        default=False, 
        help="quantize inputs"
    )
    parser.add_argument(
        "--batchnorm", 
        action="store_true", 
        default=False, 
        help="Add batchnorm before quantized activations"
    )
    parser.add_argument(
        "--act1_bitwidth",
        type=int,
        default=12,
        help="bitwidth for first quantized activation in the encoder"
    )
    parser.add_argument(
        "--act2_bitwidth",
        type=int,
        default=10,
        help="bitwidth for second quantized activation in the encoder"
    )
    parser.add_argument(
        "--qinput_bitwidth",
        type=int,
        default=11,
        help="bitwidth for quantized input in the encoder"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=1e-3,
        help="Initial learning rate",
    )
    parser.add_argument(
        "--weight_decay",
        type=float,
        default=0.0, # no decay by default
        help="weight decay coefficient",
    )
    parser.add_argument(
        "--cos_anneal_warm_restarts",
        action="store_true",
        default=False,
        help="Using Cosine Annealing with Warm Restarts lr scheduler",
    )
    parser.add_argument(
        "--warm_restart_freq",
        type=int,
        default=50,
        help="Warm restart frequency in epochs"
    )
    parser.add_argument(
        "--dense_only",
        action="store_true",
        default=False,
        help="Build encoder only using Dense layers"
    )
    parser.add_argument(
        "--num_dense_feat",
        type=int,
        default=16,
        help="Number of output features for first dense layer when using dense only model"
    )

    # Add dataset-specific args
    parser = AutoEncoderDataModule.add_argparse_args(parser)

    args = parser.parse_args()
    main(args)
