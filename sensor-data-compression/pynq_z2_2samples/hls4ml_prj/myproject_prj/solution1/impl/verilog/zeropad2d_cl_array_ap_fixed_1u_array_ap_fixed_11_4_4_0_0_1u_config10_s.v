// ==============================================================
// RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and OpenCL
// Version: 2020.1
// Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module zeropad2d_cl_array_ap_fixed_1u_array_ap_fixed_11_4_4_0_0_1u_config10_s (
        ap_clk,
        ap_rst,
        ap_start,
        start_full_n,
        ap_done,
        ap_continue,
        ap_idle,
        ap_ready,
        start_out,
        start_write,
        data_V_data_V_TDATA,
        data_V_data_V_TVALID,
        data_V_data_V_TREADY,
        res_V_data_V_din,
        res_V_data_V_full_n,
        res_V_data_V_write
);

parameter    ap_ST_fsm_state1 = 4'd1;
parameter    ap_ST_fsm_state2 = 4'd2;
parameter    ap_ST_fsm_state3 = 4'd4;
parameter    ap_ST_fsm_state4 = 4'd8;

input   ap_clk;
input   ap_rst;
input   ap_start;
input   start_full_n;
output   ap_done;
input   ap_continue;
output   ap_idle;
output   ap_ready;
output   start_out;
output   start_write;
input  [15:0] data_V_data_V_TDATA;
input   data_V_data_V_TVALID;
output   data_V_data_V_TREADY;
output  [10:0] res_V_data_V_din;
input   res_V_data_V_full_n;
output   res_V_data_V_write;

reg ap_done;
reg ap_idle;
reg start_write;
reg data_V_data_V_TREADY;
reg[10:0] res_V_data_V_din;
reg res_V_data_V_write;

reg    real_start;
reg    start_once_reg;
reg    ap_done_reg;
(* fsm_encoding = "none" *) reg   [3:0] ap_CS_fsm;
wire    ap_CS_fsm_state1;
reg    internal_ap_ready;
reg    data_V_data_V_TDATA_blk_n;
wire    ap_CS_fsm_state3;
wire   [0:0] icmp_ln65_fu_129_p2;
reg    res_V_data_V_blk_n;
wire    ap_CS_fsm_state4;
wire   [0:0] icmp_ln77_fu_146_p2;
wire   [3:0] i_fu_123_p2;
reg   [3:0] i_reg_161;
wire    ap_CS_fsm_state2;
wire   [3:0] j_1_fu_135_p2;
reg    ap_block_state3;
wire   [3:0] j_fu_152_p2;
reg    ap_block_state4;
reg   [3:0] i1_0_reg_84;
reg    ap_block_state1;
reg   [3:0] j3_0_reg_95;
wire   [0:0] icmp_ln59_fu_117_p2;
reg   [3:0] j6_0_reg_106;
wire   [10:0] tmp_data_0_V_fu_141_p1;
reg   [3:0] ap_NS_fsm;
wire    regslice_both_data_V_data_V_U_apdone_blk;
wire   [15:0] data_V_data_V_TDATA_int;
wire    data_V_data_V_TVALID_int;
reg    data_V_data_V_TREADY_int;
wire    regslice_both_data_V_data_V_U_ack_in;

// power-on initialization
initial begin
#0 start_once_reg = 1'b0;
#0 ap_done_reg = 1'b0;
#0 ap_CS_fsm = 4'd1;
end

regslice_both #(
    .DataWidth( 16 ))
regslice_both_data_V_data_V_U(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst),
    .data_in(data_V_data_V_TDATA),
    .vld_in(data_V_data_V_TVALID),
    .ack_in(regslice_both_data_V_data_V_U_ack_in),
    .data_out(data_V_data_V_TDATA_int),
    .vld_out(data_V_data_V_TVALID_int),
    .ack_out(data_V_data_V_TREADY_int),
    .apdone_blk(regslice_both_data_V_data_V_U_apdone_blk)
);

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_CS_fsm <= ap_ST_fsm_state1;
    end else begin
        ap_CS_fsm <= ap_NS_fsm;
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_done_reg <= 1'b0;
    end else begin
        if ((ap_continue == 1'b1)) begin
            ap_done_reg <= 1'b0;
        end else if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state4))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        start_once_reg <= 1'b0;
    end else begin
        if (((internal_ap_ready == 1'b0) & (real_start == 1'b1))) begin
            start_once_reg <= 1'b1;
        end else if ((internal_ap_ready == 1'b1)) begin
            start_once_reg <= 1'b0;
        end
    end
end

always @ (posedge ap_clk) begin
    if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state3))) begin
        i1_0_reg_84 <= i_reg_161;
    end else if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        i1_0_reg_84 <= 4'd0;
    end
end

always @ (posedge ap_clk) begin
    if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3))) begin
        j3_0_reg_95 <= j_1_fu_135_p2;
    end else if (((icmp_ln59_fu_117_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state2))) begin
        j3_0_reg_95 <= 4'd0;
    end
end

always @ (posedge ap_clk) begin
    if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state4))) begin
        j6_0_reg_106 <= j_fu_152_p2;
    end else if (((icmp_ln59_fu_117_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state2))) begin
        j6_0_reg_106 <= 4'd0;
    end
end

always @ (posedge ap_clk) begin
    if ((1'b1 == ap_CS_fsm_state2)) begin
        i_reg_161 <= i_fu_123_p2;
    end
end

always @ (*) begin
    if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state4))) begin
        ap_done = 1'b1;
    end else begin
        ap_done = ap_done_reg;
    end
end

always @ (*) begin
    if (((real_start == 1'b0) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if (((icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3))) begin
        data_V_data_V_TDATA_blk_n = data_V_data_V_TVALID_int;
    end else begin
        data_V_data_V_TDATA_blk_n = 1'b1;
    end
end

always @ (*) begin
    if (((data_V_data_V_TVALID == 1'b1) & (regslice_both_data_V_data_V_U_ack_in == 1'b1))) begin
        data_V_data_V_TREADY = 1'b1;
    end else begin
        data_V_data_V_TREADY = 1'b0;
    end
end

always @ (*) begin
    if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3))) begin
        data_V_data_V_TREADY_int = 1'b1;
    end else begin
        data_V_data_V_TREADY_int = 1'b0;
    end
end

always @ (*) begin
    if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state4))) begin
        internal_ap_ready = 1'b1;
    end else begin
        internal_ap_ready = 1'b0;
    end
end

always @ (*) begin
    if (((start_once_reg == 1'b0) & (start_full_n == 1'b0))) begin
        real_start = 1'b0;
    end else begin
        real_start = ap_start;
    end
end

always @ (*) begin
    if ((((icmp_ln77_fu_146_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state4)) | ((icmp_ln65_fu_129_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state3)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3)))) begin
        res_V_data_V_blk_n = res_V_data_V_full_n;
    end else begin
        res_V_data_V_blk_n = 1'b1;
    end
end

always @ (*) begin
    if (((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state4)) | (~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state3)))) begin
        res_V_data_V_din = 11'd0;
    end else if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3))) begin
        res_V_data_V_din = tmp_data_0_V_fu_141_p1;
    end else begin
        res_V_data_V_din = 'bx;
    end
end

always @ (*) begin
    if (((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state4)) | (~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state3)) | (~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3)))) begin
        res_V_data_V_write = 1'b1;
    end else begin
        res_V_data_V_write = 1'b0;
    end
end

always @ (*) begin
    if (((start_once_reg == 1'b0) & (real_start == 1'b1))) begin
        start_write = 1'b1;
    end else begin
        start_write = 1'b0;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_state1 : begin
            if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end
        end
        ap_ST_fsm_state2 : begin
            if (((icmp_ln59_fu_117_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state2))) begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end
        end
        ap_ST_fsm_state3 : begin
            if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state3))) begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end else if ((~(((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0))) & (icmp_ln65_fu_129_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state3))) begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end
        end
        ap_ST_fsm_state4 : begin
            if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state4))) begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end else if ((~((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) & (icmp_ln77_fu_146_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state4))) begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign ap_CS_fsm_state1 = ap_CS_fsm[32'd0];

assign ap_CS_fsm_state2 = ap_CS_fsm[32'd1];

assign ap_CS_fsm_state3 = ap_CS_fsm[32'd2];

assign ap_CS_fsm_state4 = ap_CS_fsm[32'd3];

always @ (*) begin
    ap_block_state1 = ((real_start == 1'b0) | (ap_done_reg == 1'b1));
end

always @ (*) begin
    ap_block_state3 = (((icmp_ln65_fu_129_p2 == 1'd1) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0)) | ((icmp_ln65_fu_129_p2 == 1'd0) & (data_V_data_V_TVALID_int == 1'b0)));
end

always @ (*) begin
    ap_block_state4 = ((icmp_ln77_fu_146_p2 == 1'd0) & (res_V_data_V_full_n == 1'b0));
end

assign ap_ready = internal_ap_ready;

assign i_fu_123_p2 = (i1_0_reg_84 + 4'd1);

assign icmp_ln59_fu_117_p2 = ((i1_0_reg_84 == 4'd8) ? 1'b1 : 1'b0);

assign icmp_ln65_fu_129_p2 = ((j3_0_reg_95 == 4'd8) ? 1'b1 : 1'b0);

assign icmp_ln77_fu_146_p2 = ((j6_0_reg_106 == 4'd9) ? 1'b1 : 1'b0);

assign j_1_fu_135_p2 = (j3_0_reg_95 + 4'd1);

assign j_fu_152_p2 = (j6_0_reg_106 + 4'd1);

assign start_out = real_start;

assign tmp_data_0_V_fu_141_p1 = data_V_data_V_TDATA_int[10:0];

endmodule //zeropad2d_cl_array_ap_fixed_1u_array_ap_fixed_11_4_4_0_0_1u_config10_s
