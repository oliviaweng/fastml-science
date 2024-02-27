#ifndef NNET_INSTR_GEN_H_
#define NNET_INSTR_GEN_H_

#include "nnet_helpers.h"
#include <iostream>

namespace nnet {

template <class data_T, typename CONFIG_T> class FillConv1DBuffer {
  public:
    static void fill_buffer(data_T data[CONFIG_T::in_width * CONFIG_T::n_chan],
                            data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_width * CONFIG_T::n_chan],
                            const unsigned partition) {
        // To be implemented in subclasses
    }
};

template <class data_T, typename CONFIG_T> class FillConv2DBuffer {
  public:
    static void
    fill_buffer(data_T data[CONFIG_T::in_height * CONFIG_T::in_width * CONFIG_T::n_chan],
                data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_height * CONFIG_T::filt_width * CONFIG_T::n_chan],
                const unsigned partition) {
        // To be implemented in subclasses
    }
};

// hls4ml insert code
template<class data_T, typename CONFIG_T>
class fill_buffer_3 : public FillConv2DBuffer<data_T, CONFIG_T> {
    public:
    static void fill_buffer(
        data_T data[CONFIG_T::in_height * CONFIG_T::in_width * CONFIG_T::n_chan],
        data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_height * CONFIG_T::filt_width * CONFIG_T::n_chan],
        const unsigned partition
    ) {
        if (partition ==   0) {
            buffer[0][0] =    data[0]; buffer[0][1] =    data[1]; buffer[0][2] =    data[2]; buffer[0][3] =    data[8]; buffer[0][4] =    data[9]; buffer[0][5] =   data[10]; buffer[0][6] =   data[16]; buffer[0][7] =   data[17]; buffer[0][8] =   data[18];

        }
        if (partition ==   1) {
            buffer[0][0] =    data[2]; buffer[0][1] =    data[3]; buffer[0][2] =    data[4]; buffer[0][3] =   data[10]; buffer[0][4] =   data[11]; buffer[0][5] =   data[12]; buffer[0][6] =   data[18]; buffer[0][7] =   data[19]; buffer[0][8] =   data[20];

        }
        if (partition ==   2) {
            buffer[0][0] =    data[4]; buffer[0][1] =    data[5]; buffer[0][2] =    data[6]; buffer[0][3] =   data[12]; buffer[0][4] =   data[13]; buffer[0][5] =   data[14]; buffer[0][6] =   data[20]; buffer[0][7] =   data[21]; buffer[0][8] =   data[22];

        }
        if (partition ==   3) {
            buffer[0][0] =    data[6]; buffer[0][1] =    data[7]; buffer[0][2] =          0; buffer[0][3] =   data[14]; buffer[0][4] =   data[15]; buffer[0][5] =          0; buffer[0][6] =   data[22]; buffer[0][7] =   data[23]; buffer[0][8] =          0;

        }
        if (partition ==   4) {
            buffer[0][0] =   data[16]; buffer[0][1] =   data[17]; buffer[0][2] =   data[18]; buffer[0][3] =   data[24]; buffer[0][4] =   data[25]; buffer[0][5] =   data[26]; buffer[0][6] =   data[32]; buffer[0][7] =   data[33]; buffer[0][8] =   data[34];

        }
        if (partition ==   5) {
            buffer[0][0] =   data[18]; buffer[0][1] =   data[19]; buffer[0][2] =   data[20]; buffer[0][3] =   data[26]; buffer[0][4] =   data[27]; buffer[0][5] =   data[28]; buffer[0][6] =   data[34]; buffer[0][7] =   data[35]; buffer[0][8] =   data[36];

        }
        if (partition ==   6) {
            buffer[0][0] =   data[20]; buffer[0][1] =   data[21]; buffer[0][2] =   data[22]; buffer[0][3] =   data[28]; buffer[0][4] =   data[29]; buffer[0][5] =   data[30]; buffer[0][6] =   data[36]; buffer[0][7] =   data[37]; buffer[0][8] =   data[38];

        }
        if (partition ==   7) {
            buffer[0][0] =   data[22]; buffer[0][1] =   data[23]; buffer[0][2] =          0; buffer[0][3] =   data[30]; buffer[0][4] =   data[31]; buffer[0][5] =          0; buffer[0][6] =   data[38]; buffer[0][7] =   data[39]; buffer[0][8] =          0;

        }
        if (partition ==   8) {
            buffer[0][0] =   data[32]; buffer[0][1] =   data[33]; buffer[0][2] =   data[34]; buffer[0][3] =   data[40]; buffer[0][4] =   data[41]; buffer[0][5] =   data[42]; buffer[0][6] =   data[48]; buffer[0][7] =   data[49]; buffer[0][8] =   data[50];

        }
        if (partition ==   9) {
            buffer[0][0] =   data[34]; buffer[0][1] =   data[35]; buffer[0][2] =   data[36]; buffer[0][3] =   data[42]; buffer[0][4] =   data[43]; buffer[0][5] =   data[44]; buffer[0][6] =   data[50]; buffer[0][7] =   data[51]; buffer[0][8] =   data[52];

        }
        if (partition ==  10) {
            buffer[0][0] =   data[36]; buffer[0][1] =   data[37]; buffer[0][2] =   data[38]; buffer[0][3] =   data[44]; buffer[0][4] =   data[45]; buffer[0][5] =   data[46]; buffer[0][6] =   data[52]; buffer[0][7] =   data[53]; buffer[0][8] =   data[54];

        }
        if (partition ==  11) {
            buffer[0][0] =   data[38]; buffer[0][1] =   data[39]; buffer[0][2] =          0; buffer[0][3] =   data[46]; buffer[0][4] =   data[47]; buffer[0][5] =          0; buffer[0][6] =   data[54]; buffer[0][7] =   data[55]; buffer[0][8] =          0;

        }
        if (partition ==  12) {
            buffer[0][0] =   data[48]; buffer[0][1] =   data[49]; buffer[0][2] =   data[50]; buffer[0][3] =   data[56]; buffer[0][4] =   data[57]; buffer[0][5] =   data[58]; buffer[0][6] =          0; buffer[0][7] =          0; buffer[0][8] =          0;

        }
        if (partition ==  13) {
            buffer[0][0] =   data[50]; buffer[0][1] =   data[51]; buffer[0][2] =   data[52]; buffer[0][3] =   data[58]; buffer[0][4] =   data[59]; buffer[0][5] =   data[60]; buffer[0][6] =          0; buffer[0][7] =          0; buffer[0][8] =          0;

        }
        if (partition ==  14) {
            buffer[0][0] =   data[52]; buffer[0][1] =   data[53]; buffer[0][2] =   data[54]; buffer[0][3] =   data[60]; buffer[0][4] =   data[61]; buffer[0][5] =   data[62]; buffer[0][6] =          0; buffer[0][7] =          0; buffer[0][8] =          0;

        }
        if (partition ==  15) {
            buffer[0][0] =   data[54]; buffer[0][1] =   data[55]; buffer[0][2] =          0; buffer[0][3] =   data[62]; buffer[0][4] =   data[63]; buffer[0][5] =          0; buffer[0][6] =          0; buffer[0][7] =          0; buffer[0][8] =          0;

        }
    }
};

} // namespace nnet

#endif
