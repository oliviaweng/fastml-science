import torch
import torch.nn as nn
import pytorch_lightning as pl

from telescope_pt import telescopeMSE8x8
from utils.metrics import emd

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
"""

class AutoEncoder(pl.LightningModule):
    """
    XDR AutoEncoder class
    """
    def __init__(self) -> None:
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(128, 16),
        )

        self.decoder = nn.Sequential(
            nn.Linear(16, 128),
            nn.ReLU(),
            nn.Unflatten(1, (8, 8, 8)),
            nn.ConvTranspose2d(8, 1, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid(),
        )
        self.loss = telescopeMSE8x8
    
    def map_to_calq(self, x):
        """
        Map the input/output of the autoencoder into CALQs orders
        """
        return x.reshape(len(x), 48)


    # Pytorch Lightning specific methods
    def forward(self, x):
        return self.decoder(self.encoder(x))

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def training_step(self, batch, batch_idx):
        x, y = batch
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        self.log('train_loss', loss)
        return loss 
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        self.log('val_loss', loss)
        return loss
    
    def test_step(self, batch, batch_idx):
        x, y = batch
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        self.log('test_loss', loss)
        return loss



"""
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