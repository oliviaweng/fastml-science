#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_fixed.h"
#include "ap_int.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

// hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 8
#define N_INPUT_2_1 8
#define N_INPUT_3_1 1
#define OUT_HEIGHT_10 9
#define OUT_WIDTH_10 9
#define N_CHAN_10 1
#define OUT_HEIGHT_3 4
#define OUT_WIDTH_3 4
#define N_FILT_3 8
#define OUT_HEIGHT_3 4
#define OUT_WIDTH_3 4
#define N_FILT_3 8
#define N_SIZE_0_6 128
#define N_LAYER_7 16
#define N_LAYER_7 16

// hls-fpga-machine-learning insert layer-precision
typedef nnet::array<ap_fixed<11,4,AP_RND_CONV,AP_SAT>, 1*1> input_t;
typedef nnet::array<ap_fixed<11,4,AP_RND_CONV,AP_SAT>, 1*1> layer10_t;
typedef ap_fixed<16,6> model_default_t;
typedef nnet::array<ap_fixed<16,6>, 8*1> layer3_t;
typedef ap_fixed<6,2> weight3_t;
typedef ap_fixed<6,2> bias3_t;
typedef nnet::array<ap_ufixed<12,3,AP_RND_CONV,AP_SAT>, 8*1> layer5_t;
typedef ap_fixed<18,8> accum1_qa_table_t;
typedef nnet::array<ap_fixed<16,6>, 16*1> layer7_t;
typedef ap_fixed<6,2> weight7_t;
typedef ap_fixed<6,2> bias7_t;
typedef ap_uint<1> layer7_index;
typedef nnet::array<ap_ufixed<9,1,AP_RND_CONV,AP_SAT>, 16*1> result_t;
typedef ap_fixed<18,8> encod_qa_table_t;

#endif
