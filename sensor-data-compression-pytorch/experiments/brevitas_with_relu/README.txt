These experiments are run with the original model topology of the autoencoder
(including the last relu layer). We do not move forward with this model because 
it has a somewhat unstable training recipe. We are instead moving forward with
a version of the model where we remove the last relu in the encoder, which 
performs better and has more stable EMD. 

Date: Sept 15, 2023