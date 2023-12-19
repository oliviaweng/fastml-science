import torch
import torch.nn as nn
import brevitas.nn as qnn
from brevitas.quant import Int8BiasPerTensorFixedPointInternalScaling
from brevitas.inject.enum import QuantType, ScalingImplType
import pytorch_lightning as pl

from collections import OrderedDict
from telescope_pt import telescopeMSE8x8, move_constants_to_gpu
from autoencoder_datamodule import ARRANGE, ARRANGE_MASK


"""
QKeras model

Model: "encoder"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 8, 8, 1)]         0         
                                                                 
 input_qa (QActivation)      (None, 8, 8, 1)           0         
                                                                 
 conv2d_0_m (FQConv2D)       (None, 4, 4, 8)           80        
                                                                 
 accum1_qa (QActivation)     (None, 4, 4, 8)           0         
                                                                 
 flatten (Flatten)           (None, 128)               0         
                                                                 
 encoded_vector (FQDense)    (None, 16)                2064      
                                                                 
 encod_qa (QActivation)      (None, 16)                0         
                                                                 
=================================================================
Total params: 2,144
Trainable params: 2,144
Non-trainable params: 0

_________________________________________________________________
Model: "decoder"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 decoder_input (InputLayer)  [(None, 16)]              0         
                                                                 
 de_dense_final (Dense)      (None, 128)               2176      
                                                                 
 de_reshape (Reshape)        (None, 4, 4, 8)           0         
                                                                 
 conv2D_t_0 (Conv2DTranspose  (None, 8, 8, 8)          584       
 )                                                               
                                                                 
 conv2d_t_final (Conv2DTrans  (None, 8, 8, 1)          73        
 pose)                                                           
                                                                 
 decoder_output (Activation)  (None, 8, 8, 1)          0         
                                                                 
=================================================================
Total params: 2,833
Trainable params: 2,833
Non-trainable params: 0
"""


CALQ_MASK = torch.tensor(
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
    ]
)


class AutoEncoder(pl.LightningModule):
    """
    XDR AutoEncoder class
    """

    def __init__(
            self, 
            batchnorm=False,
            accelerator="gpu", 
            learning_rate=1e-3,
            quantize_act=False, 
            quantize_input=False,
            quantize_weight=False,
            act1_bitwidth=12,
            qinput_bitwidth=11,
            act2_bitwidth=10,
            weight_decay=0.0,
            cos_anneal_warm_restarts=False,
            warm_restart_freq=50, # in epochs
            dense_only=False, # Dense layers only
            num_dense_feat=16,
            input_size=64, # Size of input (64 for convolution)
    ) -> None:
        super().__init__()
        self.save_hyperparameters()

        self.encoded_dim = 16
        self.shape = (1, 8, 8)  # PyTorch defaults to (C, H, W)
        self.val_sum = None
        self.lr = learning_rate
        self.batchnorm = batchnorm
        self.accelerator = accelerator
        self.quantize_act = quantize_act
        self.quantize_input = quantize_input
        self.act1_bitwidth = act1_bitwidth
        self.quantize_weight = quantize_weight
        self.qinput_bitwidth = qinput_bitwidth
        self.act2_bitwidth = act2_bitwidth
        self.weight_decay = weight_decay
        self.cos_anneal_warm_restarts = cos_anneal_warm_restarts
        self.warm_restart_freq = warm_restart_freq
        self.dense_only = dense_only
        self.num_dense_feat = num_dense_feat

        # Build encoder
        layers = OrderedDict()

        # Quantize input if necessary
        if self.quantize_input:
            print("Quantizing inputs!")
            self.input_quant = qnn.QuantIdentity(
                bit_width=self.qinput_bitwidth, 
                quant_type=QuantType.INT, 
                # return quant tensors when quantizing the weights
                return_quant_tensor=self.quantize_weight,
            ) 
            layers["input_quant"] = self.input_quant

        if dense_only: # Build model with linear layers only
            print("Building dense only model!")
            layers["flatten"] = nn.Flatten()
            layers["dense1"] = nn.Linear(64, self.num_dense_feat)
            if self.batchnorm:
                print("Using batchnorm!")
                layers["bn1"] = nn.BatchNorm1d(self.num_dense_feat)
            if self.quantize_act:
                print("Quantizing activations!")
                layers["qrelu1"] =  qnn.QuantReLU(
                    bit_width=self.act1_bitwidth, 
                    quant_type=QuantType.INT, 
                    # scaling_impl_type=ScalingImplType.PARAMETER,
                )
            else:
                layers["relu1"] = nn.ReLU()
            layers["dense2"] = nn.Linear(self.num_dense_feat, self.encoded_dim)
            if self.batchnorm:
                layers["bn2"] = nn.BatchNorm1d(self.encoded_dim)
            if self.quantize_act:
                layers["qidentity"] =  qnn.QuantIdentity(
                    bit_width=self.act2_bitwidth, 
                    quant_type=QuantType.INT, 
                    # scaling_impl_type=ScalingImplType.PARAMETER,
                )
        else: # Use Conv2d as first layer
            if self.quantize_weight:
                print("Quantizing weights!")
                layers["conv"] =  qnn.QuantConv2d(
                    1, 
                    8, 
                    kernel_size=3, 
                    stride=2, 
                    padding=1, 
                    weight_bit_width=6, 
                    quant_type=QuantType.INT,
                    # bias_quant=??
                ) 
            else:
                layers["conv"] = nn.Conv2d(1, 8, kernel_size=3, stride=2, padding=1)
            if self.batchnorm:
                print("Using batchnorm!")
                layers["bn1"] = nn.BatchNorm2d(8)
            # Relu activation
            if quantize_act:
                print("Quantizing activations!")
                layers["qrelu"] =  qnn.QuantReLU(
                    bit_width=self.act1_bitwidth, 
                    quant_type=QuantType.INT, 
                    # return quant tensors when quantizing the weights
                    return_quant_tensor=self.quantize_weight,
                    # scaling_impl_type=ScalingImplType.PARAMETER,
                )
            else:
                layers["relu"] = nn.ReLU()

            layers["flatten"] = nn.Flatten()
            # Linear Layer
            if self.quantize_weight:
                layers["enc_dense"] = qnn.QuantLinear(
                    128, 
                    self.encoded_dim, 
                    bias=True,
                    weight_bit_width=6, 
                    quant_type=QuantType.INT,
                    # bias_quant=??
                )
            else:
                layers["enc_dense"] = nn.Linear(128, self.encoded_dim)
            if self.batchnorm:
                layers["bn2"] = nn.BatchNorm1d(self.encoded_dim)
            # Quantized identity if necessary
            if self.quantize_act:
                layers["qlinear_act"] = qnn.QuantIdentity(
                    bit_width=self.act2_bitwidth,
                    quant_type=QuantType.INT, # FP = float32 
                    # return quant tensors when quantizing the weights
                    return_quant_tensor=self.quantize_weight,
                    # scaling_impl_type=ScalingImplType.PARAMETER,
                ) 

        self.encoder = nn.Sequential(layers)

        if self.dense_only: # Decoder for dense-only model
            self.decoder = nn.Sequential(OrderedDict([
                ("dec_dense", nn.Linear(self.encoded_dim, self.num_dense_feat)),
                ("relu1", nn.ReLU()),
                ("dense_final", nn.Linear(self.num_dense_feat, 64)), 
                ("relu2", nn.ReLU()),
                ("unflatten", nn.Unflatten(1, (1, 8, 8))),
                (
                    "convtrans2d",
                    nn.ConvTranspose2d(
                        1,
                        self.shape[0],
                        kernel_size=3,
                        stride=1,
                        padding=1,
                    ),
                ),
                ("sigmoid", nn.Sigmoid()),
            ]))
        else: # Decoder for conv2d model
            self.decoder = nn.Sequential(OrderedDict([
                ("dec_dense", nn.Linear(self.encoded_dim, 128)),
                ("relu1", nn.ReLU()),
                ("unflatten", nn.Unflatten(1, (8, 4, 4))),
                (
                    "convtrans2d1",
                    nn.ConvTranspose2d(
                        8, 8, kernel_size=3, stride=2, padding=1, output_padding=1
                    ),
                ),
                ("relu2", nn.ReLU()),
                (
                    "convtrans2d2",
                    nn.ConvTranspose2d(
                        8,
                        self.shape[0],
                        kernel_size=3,
                        stride=1,
                        padding=1,
                    ),
                ),
                ("sigmoid", nn.Sigmoid()),
            ]))
        self.loss = telescopeMSE8x8
        if accelerator == "gpu":
            move_constants_to_gpu()

    def invert_arrange(self):
        """
        Invert the arrange mask
        """
        remap = []
        hashmap = {}  # cell : index mapping
        found_duplicate_charge = len(ARRANGE[ARRANGE_MASK == 1]) > len(
            torch.unique(ARRANGE[ARRANGE_MASK == 1])
        )
        for i in range(len(ARRANGE)):
            if ARRANGE_MASK[i] == 1:
                if found_duplicate_charge:
                    if CALQ_MASK[i] == 1:
                        hashmap[int(ARRANGE[i])] = i
                else:
                    hashmap[int(ARRANGE[i])] = i
        for i in range(len(torch.unique(ARRANGE))):
            remap.append(hashmap[i])
        return torch.tensor(remap)

    def map_to_calq(self, x):
        """
        Map the input/output of the autoencoder into CALQs orders
        """
        remap = self.invert_arrange()
        image_size = self.shape[0] * self.shape[1] * self.shape[2]
        reshaped_x = x.reshape(len(x), image_size)
        reshaped_x[:, ARRANGE_MASK == 0] = 0
        return reshaped_x[:, remap]

    def set_val_sum(self, val_sum):
        self.val_sum = val_sum

    def predict(self, x):
        decoded_Q = self(x)
        encoded_Q = self.encoder(x)
        encoded_Q = torch.reshape(encoded_Q, (len(encoded_Q), self.encoded_dim, 1))
        return decoded_Q, encoded_Q
    
    def filter_weight_decay_params(self, no_decay_keys=["bn", "bias", "scaling_impl"]):
        """
        By default, turn off weight decay for batch norm, bias, and brevitas learned scaling values
        """
        decay_params = set()
        no_decay_params = set()
        for name, param in self.named_parameters():
            if param.requires_grad:
                no_decay_param_found = False
                for k in no_decay_keys:
                    if k in name:
                        no_decay_params.add(param)
                        no_decay_param_found = True
                if not no_decay_param_found:
                    decay_params.add(param)
        return list(decay_params), list(no_decay_params)

    # Pytorch Lightning specific methods
    def forward(self, x):
        return self.decoder(self.encoder(x))

    def configure_optimizers(self):
        # Remove batchnorm params and bias from weight decay
        if self.weight_decay > 0:
            print(f"Training with weight decay = {self.weight_decay}!")
            decay_params, no_decay_params = self.filter_weight_decay_params()
            params = [
                {
                    "params": decay_params,
                    "weight_decay": self.weight_decay,
                },
                {
                    "params": no_decay_params,
                    "weight_decay": 0.0
                },
            ]
        else:
            params = self.parameters()
        optimizer = torch.optim.AdamW(params, lr=self.lr)
        # TODO: Add flag check to toggle scheduler on and off
        if self.cos_anneal_warm_restarts:
            scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
                optimizer, T_0=self.warm_restart_freq,
            )
            return [optimizer], [scheduler]
        return optimizer

    def training_step(self, batch, batch_idx):

        x = batch
        x_hat = self(x)
        loss = self.loss(x, x_hat)
        self.log("train_loss", loss, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x = batch
        x_hat = self(x)
        loss = self.loss(x, x_hat)
        self.log("val_loss", loss, on_epoch=True, prog_bar=True)
        return loss
