import argparse
import matplotlib.pyplot as plt

from autoencoder import AutoEncoder

# Plot a histogram of the weights
def plot_weights(model, filename, encoder_only):
    for name, params in model.named_parameters():
        if "weight" in name:
            if encoder_only:
                if "encoder" in name:
                    plt.hist(params.detach().numpy().flatten(), label=name, alpha=0.5)
            else:
                plt.hist(params.detach().numpy().flatten(), label=name, alpha=0.5)
    plt.legend()
    plt.savefig(f"plots/{filename}.pdf")


def main(args):
    model = AutoEncoder()
    model.load_from_checkpoint(args.checkpoint)
    plot_weights(model, args.filename, args.encoder_only)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot model weights")
    parser.add_argument("--checkpoint", type=str, help="Path to model checkpoint")
    parser.add_argument(
        "--filename", type=str, default="test", help="Filename to save plot"
    )
    parser.add_argument(
        "--encoder-only",
        action="store_true",
        default=False,
        help="Only plot encoder weights",
    )
    args = parser.parse_args()
    main(args)
