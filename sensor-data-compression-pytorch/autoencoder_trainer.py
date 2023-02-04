import os
import torchinfo
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint, ModelSummary
from argparse import ArgumentParser
from autoencoder import AutoEncoder
from autoencoder_datamodule import AutoEncoderDataModule


def main(args):
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
    model = AutoEncoder(accelerator=args.accelerator)
    torchinfo.summary(model, input_size=(1, 1, 8, 8))  # (B, C, H, W)


    tb_logger = pl_loggers.TensorBoardLogger(
        args.save_dir, name=args.experiment_name
    )

    # Save top-3 checkpoints based on Val/Loss
    top3_checkpoint_callback = ModelCheckpoint(
        save_top_k=3,
        save_last=True,
        monitor="val_loss",
        mode="min",
        dirpath=os.path.join(args.save_dir, args.experiment_name),
        filename=f"{args.experiment_name}" "_epoch={epoch:02d}_loss={val_loss:.3f}",
        auto_insert_metric_name=False,
    )

    # ------------------------
    # 2 INIT TRAINER
    # ------------------------
    trainer = pl.Trainer(
        max_epochs=args.max_epochs,
        accelerator=args.accelerator,
        logger=tb_logger,
        callbacks=[top3_checkpoint_callback],
        fast_dev_run=args.fast_dev_run,
    )

    # ------------------------
    # 3 TRAIN MODEL
    # ------------------------
    if args.train:
        trainer.fit(model=model, datamodule=data_module)

    # ------------------------
    # 4 EVALUTE MODEL
    # ------------------------
    if args.train or args.evaluate:
        # Need val_sum to compute EMD
        _, val_sum = data_module.get_val_max_and_sum()
        model.set_val_sum(val_sum)
        test_results = trainer.test(
            model=model, datamodule=data_module, ckpt_path="last"
        )
        test_results_log = os.path.join(
            args.save_dir, args.experiment_name, args.experiment_name + "_test.txt"
        )
        with open(test_results_log, "w") as f:
            f.write(str(test_results))
            f.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--process_data", action="store_true", default=False)
    parser.add_argument("--max_epochs", type=int, default=100)
    parser.add_argument("--save_dir", type=str, default="./pt_autoencoder_test")
    parser.add_argument("--experiment_name", type=str, default="autoencoder")
    parser.add_argument("--fast_dev_run", action="store_true", default=False)
    parser.add_argument(
        "--accelerator", type=str, choices=["cpu", "gpu", "auto"], default="gpu"
    )
    parser.add_argument("--train", action="store_true", default=False)
    parser.add_argument("--evaluate", action="store_true", default=False)

    # Add dataset-specific args
    parser = AutoEncoderDataModule.add_argparse_args(parser)

    args = parser.parse_args()
    main(args)
