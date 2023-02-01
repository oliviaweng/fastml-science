import time
import torch
import numpy as np
import torch.nn as nn
import pytorch_lightning as pl

from telescope_pt import telescopeMSE8x8
from utils.metrics import emd
from utils_pt import unnormalize
from multiprocessing import Pool

"""
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


class AutoEncoder(pl.LightningModule):
    """
    XDR AutoEncoder class
    """

    def __init__(self, val_sum) -> None:
        super().__init__()

        self.encoded_dim = 16
        self.shape = (1, 8, 8) # PyTorch defaults to (C, H, W)
        self.val_sum = val_sum

        self.encoder = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(128, self.encoded_dim),
        )

        self.decoder = nn.Sequential(
            nn.Linear(self.encoded_dim, 128),
            nn.ReLU(),
            nn.Unflatten(1, self.shape),
            nn.ConvTranspose2d(
                self.shape[2], 8, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.ConvTranspose2d(
                8, self.shape[0], kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.Sigmoid(),
        )
        self.loss = telescopeMSE8x8

    def map_to_calq(self, x):
        """
        Map the input/output of the autoencoder into CALQs orders
        """
        return x.reshape(len(x), 48)

    def predict(self, x):
        decoded_Q = self(x)
        encoded_Q = self.encoder(x)
        encoded_Q = np.reshape(encoded_Q, (len(encoded_Q), self.encoded_dim, 1))
        return x, decoded_Q, encoded_Q

    # Pytorch Lightning specific methods
    def forward(self, x):
        return self.decoder(self.encoder(x))

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def training_step(self, batch, batch_idx):
        x, y = batch
        x_hat = self(x)
        loss = self.loss(x, x_hat)
        self.log("train_loss", loss, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        x_hat = self(x)
        loss = self.loss(x, x_hat)
        self.log("val_loss", loss, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        """
        TODO: Instead compute the EMD between the input and output
        """
        x, y = batch
        input_Q, cnn_deQ, cnn_enQ = self.predict(x)
        input_calQ = self.map_to_calq(input_Q)
        output_calQ_fr = self.map_to_calq(cnn_deQ)
        print(f"input_Q.shape: {input_Q.shape}")
        print(f"input_calQ.shape: {input_calQ.shape}")
        print("Restore normalization")
        # Compute EMD
        input_calQ = np.array(
            [input_calQ[i] * self.val_sum[i] for i in range(len(input_calQ))]
        )  # shape = (batch_size, 48)
        output_calQ = unnormalize(output_calQ_fr.copy(), self.val_sum)  # ae_out

        start_time = time.time()
        with Pool() as p:
            emd_list = p.starmap(emd, zip(input_calQ, output_calQ))
        print(f"EMD computation time: {time.time() - start_time}")
        average_emd = np.mean(np.array(emd_list))
        print(f"Average EMD: {average_emd}")

        loss = self.loss(x, cnn_deQ)
        metrics = {"average_emd": average_emd, "loss": loss}
        self.log_dict(metrics)
        return metrics


"""
_________________________________________________________________
Model: "autoencoder"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 8, 8, 1)]         0         
                                                                 
 encoder (Functional)        (None, 16)                2144      
                                                                 
 decoder (Functional)        (None, 8, 8, 1)           2833      
                                                                 
=================================================================
Total params: 4,977
Trainable params: 4,977
Non-trainable params: 0
"""
