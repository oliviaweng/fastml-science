import ot
import time
import torch
import torch.nn as nn
import pytorch_lightning as pl

from telescope_pt import telescopeMSE8x8, move_constants_to_gpu
from autoencoder_datamodule import ARRANGE, ARRANGE_MASK
from utils_pt import unnormalize, emd

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


CALQ_MASK = torch.tensor([
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
    1,1,1,1,0,0,0,0,
])

class AutoEncoder(pl.LightningModule):
    """
    XDR AutoEncoder class
    """

    def __init__(self, accelerator="gpu") -> None:
        super().__init__()

        self.encoded_dim = 16
        self.shape = (1, 8, 8) # PyTorch defaults to (C, H, W)
        self.val_sum = None
        self.accelerator = accelerator
        self.hex_metric = self.get_hex_metric()

        self.encoder = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(128, self.encoded_dim),
        )

        self.decoder = nn.Sequential(
            nn.Linear(self.encoded_dim, 128),
            nn.ReLU(),
            nn.Unflatten(1, (8, 4, 4)),
            nn.ConvTranspose2d(
                8, 8, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.ReLU(),
            nn.ConvTranspose2d(
                8, self.shape[0], kernel_size=3, stride=1, padding=1,
            ),
            nn.Sigmoid(),
        )
        self.loss = telescopeMSE8x8
        if accelerator == "gpu":
            print("Moved constants to gpu")
            move_constants_to_gpu()

    def invert_arrange(self):
        """
        Invert the arrange mask
        """
        remap = []
        hashmap = {} # cell : index mapping
        found_duplicate_charge = len(ARRANGE[ARRANGE_MASK == 1]) > len(torch.unique(ARRANGE[ARRANGE_MASK == 1]))
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

    # EMD constants
    def get_hex_metric(self):
        hexCoords = torch.tensor([
            [0.0, 0.0], [0.0, -2.4168015], [0.0, -4.833603], [0.0, -7.2504044],
            [2.09301, -1.2083969], [2.09301, -3.6251984], [2.09301, -6.042], [2.09301, -8.458794],
            [4.18602, -2.4168015], [4.18602, -4.833603], [4.18602, -7.2504044], [4.18602, -9.667198],
            [6.27903, -3.6251984], [6.27903, -6.042], [6.27903, -8.458794], [6.27903, -10.875603],
            [-8.37204, -10.271393], [-6.27903, -9.063004], [-4.18602, -7.854599], [-2.0930138, -6.6461945],
            [-8.37204, -7.854599], [-6.27903, -6.6461945], [-4.18602, -5.4377975], [-2.0930138, -4.229393],
            [-8.37204, -5.4377975], [-6.27903, -4.229393], [-4.18602, -3.020996], [-2.0930138, -1.8125992],
            [-8.37204, -3.020996], [-6.27903, -1.8125992], [-4.18602, -0.6042023], [-2.0930138, 0.6042023],
            [4.7092705, -12.386101], [2.6162605, -11.177696], [0.5232506, -9.969299], [-1.5697594, -8.760895],
            [2.6162605, -13.594498], [0.5232506, -12.386101], [-1.5697594, -11.177696], [-3.6627693, -9.969299],
            [0.5232506, -14.802895], [-1.5697594, -13.594498], [-3.6627693, -12.386101], [-5.7557793, -11.177696],
            [-1.5697594, -16.0113], [-3.6627693, -14.802895], [-5.7557793, -13.594498], [-7.848793, -12.386101]
        ])
        #normalize so that distance between small cells (there are 4 per TC) is 1
        oneHexCell = 0.5 * 2.4168015
        hexCoords = hexCoords / oneHexCell
        # pairwise distances
        hex_metric = ot.dist(hexCoords, hexCoords, 'euclidean')
        return hex_metric

    # Pytorch Lightning specific methods
    def forward(self, x):
        return self.decoder(self.encoder(x))

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
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

    def test_step(self, batch, batch_idx):
        """
        TODO: Instead compute the EMD between the input and output
        """
        x = batch
        cnn_deQ, cnn_enQ = self.predict(x)
        input_calQ = self.map_to_calq(x)
        output_calQ_fr = self.map_to_calq(cnn_deQ)
        # Compute EMD
        input_calQ = torch.stack(
            [input_calQ[i] * self.val_sum[i] for i in range(len(input_calQ))]
        )  # shape = (batch_size, 48)
        output_calQ = unnormalize(torch.clone(output_calQ_fr), self.val_sum)  # ae_out
        return (input_calQ, output_calQ)
    
    def test_epoch_end(self, outputs):
        input_calQ = torch.cat([output[0] for output in outputs])
        output_calQ = torch.cat([output[1] for output in outputs])
        start_time = time.time()
        emd_list = [emd(input_calQ[i], output_calQ[i], self.hex_metric) for i in range(len(input_calQ))]
        print(f"EMD computation time: {time.time() - start_time}")
        average_emd = torch.mean(torch.tensor(emd_list))
        print(f"Average EMD: {average_emd}")
        self.log("average_emd", average_emd)

