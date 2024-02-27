#include <iostream>

#include "myproject.h"
#include "parameters.h"

void myproject(
    input_t input_1[N_INPUT_1_1*N_INPUT_2_1*N_INPUT_3_1],
    result_t layer9_out[N_LAYER_7]
) {

    // hls-fpga-machine-learning insert IO
    #pragma HLS ARRAY_RESHAPE variable=input_1 complete dim=0
    #pragma HLS ARRAY_PARTITION variable=layer9_out complete dim=0
    #pragma HLS INTERFACE ap_vld port=input_1,layer9_out 
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

    layer3_t layer3_out[OUT_HEIGHT_3*OUT_WIDTH_3*N_FILT_3];
    #pragma HLS ARRAY_PARTITION variable=layer3_out complete dim=0
    nnet::conv_2d_cl<input_t, layer3_t, config3>(input_1, layer3_out, w3, b3); // conv2d_0_m
#ifndef __SYNTHESIS__
    nnet::save_layer_output<layer3_t>(layer3_out, "conv2d_0_m", OUT_HEIGHT_3*OUT_WIDTH_3*N_FILT_3);
#endif

    layer5_t layer5_out[OUT_HEIGHT_3*OUT_WIDTH_3*N_FILT_3];
    #pragma HLS ARRAY_PARTITION variable=layer5_out complete dim=0
    nnet::relu<layer3_t, layer5_t, relu_config5>(layer3_out, layer5_out); // accum1_qa
#ifndef __SYNTHESIS__
    nnet::save_layer_output<layer5_t>(layer5_out, "accum1_qa", OUT_HEIGHT_3*OUT_WIDTH_3*N_FILT_3);
#endif

    auto& layer6_out = layer5_out;
    layer7_t layer7_out[N_LAYER_7];
    #pragma HLS ARRAY_PARTITION variable=layer7_out complete dim=0
    nnet::dense<layer5_t, layer7_t, config7>(layer6_out, layer7_out, w7, b7); // encoded_vector
#ifndef __SYNTHESIS__
    nnet::save_layer_output<layer7_t>(layer7_out, "encoded_vector", N_LAYER_7);
#endif

    nnet::relu<layer7_t, result_t, relu_config9>(layer7_out, layer9_out); // encod_qa
#ifndef __SYNTHESIS__
    nnet::save_layer_output<result_t>(layer9_out, "encod_qa", N_LAYER_7);
#endif

}
