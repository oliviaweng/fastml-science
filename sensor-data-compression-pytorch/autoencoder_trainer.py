import os
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint, ModelSummary
from argparse import ArgumentParser

from autoencoder import AutoEncoder
from autoencoder_datamodule import AutoEncoderDataModule


def main(args):
    """
    Main function
    """
    # ------------------------
    # 0 PREPARE DATA
    # ------------------------

    data_module = AutoEncoderDataModule.add_argparse_args(parser)

    # ------------------------
    # 1 INIT LIGHTNING MODEL
    # ------------------------
    model = AutoEncoder()

    tb_logger = pl_loggers.TensorBoardLogger(args.save_dir, name=args.experiment_name)

    # Save top-3 checkpoints based on Val/Loss
    top3_checkpoint_callback = ModelCheckpoint(
        save_top_k=3,
        save_last=True,
        monitor="Val/Loss",
        mode="min",
        dirpath=os.path.join(args.save_dir, args.experiment_name),
        filename=f"{args.experiment_name}"
        "_epoch={epoch:02d}_loss={Val/Loss:.3f}",
        auto_insert_metric_name=False,
    )

    # ------------------------
    # 2 INIT TRAINER
    # ------------------------
    trainer = pl.Trainer(
        max_epochs=args.max_epochs,
        accelerator=args.accelerator,
        gpus=1 if args.accelerator == "gpu" else 0,
        logger=tb_logger,
        callbacks=[top3_checkpoint_callback, ModelSummary(max_depth=-1)],
        fast_dev_run=args.fast_dev_run,
    )

    # ------------------------
    # 3 START TRAINING
    # ------------------------
    trainer.fit(model=model, datamodule=data_module)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--max_epochs", type=int, default=100)
    parser.add_argument("--save_dir", type=str, default="./results")
    parser.add_argument("--experiment_name", type=str, default="autoencoder")
    parser.add_argument("--fast_dev_run", action="store_true", default=False)
    parser.add_argument(
        "--accelerator", type=str, choices=["cpu", "gpu", "auto"], default="gpu"
    )

    args = parser.parse_args()
    main(args)
