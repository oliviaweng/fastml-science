#include <iostream>

#include "myproject.h"
#include "parameters.h"

void myproject(
    hls::stream<input_t> &input_1,
    hls::stream<result_t> &layer9_out
) {

    // hls-fpga-machine-learning insert IO
    #pragma HLS INTERFACE axis port=input_1,layer9_out 
    #pragma HLS DATAFLOW 

#ifndef __SYNTHESIS__
    static bool loaded_weights = false;
    if (!loaded_weights) {
        // hls-fpga-machine-learning insert load weights
        nnet::load_weights_from_txt<weight3_t, 72>(w3, "w3.txt");
        nnet::load_weights_from_txt<bias3_t, 8>(b3, "b3.txt");
        nnet::load_weights_from_txt<weight7_t, 2048>(w7, "w7.txt");
        nnet::load_weights_from_txt<bias7_t, 16>(b7, "b7.txt");
        loaded_weights = true;
    }
#endif

    // ****************************************
    // NETWORK INSTANTIATION
    // ****************************************

    // hls-fpga-machine-learning insert layers

    hls::stream<layer10_t> layer10_out("layer10_out");
    #pragma HLS STREAM variable=layer10_out depth=81
    nnet::zeropad2d_cl<input_t, layer10_t, config10>(input_1, layer10_out); // zp2d_conv2d_0_m

    hls::stream<layer3_t> layer3_out("layer3_out");
    #pragma HLS STREAM variable=layer3_out depth=16
    nnet::conv_2d_cl<layer10_t, layer3_t, config3>(layer10_out, layer3_out, w3, b3); // conv2d_0_m

    hls::stream<layer5_t> layer5_out("layer5_out");
    #pragma HLS STREAM variable=layer5_out depth=16
    nnet::relu<layer3_t, layer5_t, relu_config5>(layer3_out, layer5_out); // accum1_qa

    auto& layer6_out = layer5_out;
    hls::stream<layer7_t> layer7_out("layer7_out");
    #pragma HLS STREAM variable=layer7_out depth=1
    nnet::dense<layer5_t, layer7_t, config7>(layer6_out, layer7_out, w7, b7); // encoded_vector

    nnet::relu<layer7_t, result_t, relu_config9>(layer7_out, layer9_out); // encod_qa

}
