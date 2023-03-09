import time
import torch
import argparse
import functorch
import numpy as np

from autoencoder import AutoEncoder
from autoencoder_datamodule import AutoEncoderDataModule

def weight_parameters(model):
    """
    Get the parameters of the model, specifically the weights.
    Return: parameters
    """
    # params = []
    # layer_shapes = {}
    # with torch.no_grad():
    #     for name, p in model.named_parameters():
    #         if p.requires_grad and "weight" in name:
    #             flat_params.append(p.flatten())
    #             layer_shapes[name] = p.shape
    # return flat_params, layer_shapes
    return [p for name, p in model.named_parameters() if "weight" in name]

def model_with_loss(model, loss):
    """
    Wrap the model with a loss function.
    """
    def model_with_loss_(input):
        output = model(input)
        return loss(input, output)
    return model_with_loss_


def loss_wrt_weights(model, ground_truth, inputs, parameters):
    """
    Parameterize the loss function with respect to the weights for Hessian 
    computation.

    parameters: List of flattened weight tensors, where layer i is initialized
                with tensor i as its weights.
    returns: scalar loss
    """
    idx = 0
    for param_name in model.state_dict():
        if "weight" in param_name:
            model.state_dict()[param_name] = parameters[idx]
            idx = idx + 1
    # for i, (name, param) in enumerate(model.named_parameters()):
    #     if param.requires_grad and "weight" in name:
    #         print(f"model.{name}")
    #         print(getattr(model, name))

    return model.loss(ground_truth, model(inputs))

def hessian(model, hessian_input, file_tag):
    """
    Compute the Hessian of each of the model's layers with respect to its
    parameters and save each Hessian matrix as its own pickle file.
    """
    start = time.time()
    single_input = hessian_input[0][None, :, :, :]
    print(f"single_input shape: {single_input.shape}")
    # single_input = single_input.cuda()
    model_output = model(single_input)
    # NOTE: autoencoder expects loss(target, output)
    target_loss = model.loss(single_input, model_output)
    print(f"Target loss = {target_loss}")

    func, params, buffers = functorch.make_functional_with_buffers(model)
    print(f"Len params = {len(params)}")
    def func_params_only(params):
        return func(params, buffers, single_input)
    hess_api = functorch.hessian(func_params_only, argnums=0)
    hess = hess_api(params)
    for h in hess:
        print(f"len h = {len(h)}")
        for t in h:
            print(f"t shape = {t.shape}")
            # print(t[0])
            # print(torch.nonzero(t))
    print(f"Hessian type: {type(hess)}")
    print(f"Hessian len: {len(hess)}")
    end = time.time()
    print(f"Time to compute Hessian: {end - start}")


def main(args):
    # Setup data
    data_module = AutoEncoderDataModule.from_argparse_args(args)
    data_module.setup("")
    hessian_input = next(iter(data_module.val_dataloader()))
    print(f"Hessian input shape: {hessian_input.shape}")

    model = AutoEncoder(accelerator="cpu").load_from_checkpoint(args.checkpoint)
    # model = model.cuda()
    model.eval()
    hessian(model, hessian_input, args.file_tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Hessian of the Autoencoder")
    parser.add_argument("--checkpoint", type=str, help="Path to model checkpoint")
    parser.add_argument(
        "--file-tag", type=str, default="test", help="Tag file used to save Hessians"
    )
    parser = AutoEncoderDataModule.add_argparse_args(parser)
    args = parser.parse_args()
    main(args)