set moduleName relu_array_ap_fixed_16u_array_ap_ufixed_9_1_4_0_0_16u_relu_config9_s
set isTopModule 0
set isTaskLevelControl 1
set isCombinational 0
set isDatapathOnly 0
set isFreeRunPipelineModule 0
set isPipelined 1
set pipeline_type function
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set C_modelName {relu<array<ap_fixed,16u>,array<ap_ufixed<9,1,4,0,0>,16u>,relu_config9>}
set C_modelType { void 0 }
set C_modelArgList {
	{ data_V_data_0_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_1_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_2_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_3_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_4_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_5_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_6_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_7_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_8_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_9_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_10_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_11_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_12_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_13_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_14_V int 16 regular {fifo 0 volatile }  }
	{ data_V_data_15_V int 16 regular {fifo 0 volatile }  }
	{ res_V_data_0_V int 16 regular {axi_s 1 volatile  { res_V_data_0_V Data } }  }
	{ res_V_data_1_V int 16 regular {axi_s 1 volatile  { res_V_data_1_V Data } }  }
	{ res_V_data_2_V int 16 regular {axi_s 1 volatile  { res_V_data_2_V Data } }  }
	{ res_V_data_3_V int 16 regular {axi_s 1 volatile  { res_V_data_3_V Data } }  }
	{ res_V_data_4_V int 16 regular {axi_s 1 volatile  { res_V_data_4_V Data } }  }
	{ res_V_data_5_V int 16 regular {axi_s 1 volatile  { res_V_data_5_V Data } }  }
	{ res_V_data_6_V int 16 regular {axi_s 1 volatile  { res_V_data_6_V Data } }  }
	{ res_V_data_7_V int 16 regular {axi_s 1 volatile  { res_V_data_7_V Data } }  }
	{ res_V_data_8_V int 16 regular {axi_s 1 volatile  { res_V_data_8_V Data } }  }
	{ res_V_data_9_V int 16 regular {axi_s 1 volatile  { res_V_data_9_V Data } }  }
	{ res_V_data_10_V int 16 regular {axi_s 1 volatile  { res_V_data_10_V Data } }  }
	{ res_V_data_11_V int 16 regular {axi_s 1 volatile  { res_V_data_11_V Data } }  }
	{ res_V_data_12_V int 16 regular {axi_s 1 volatile  { res_V_data_12_V Data } }  }
	{ res_V_data_13_V int 16 regular {axi_s 1 volatile  { res_V_data_13_V Data } }  }
	{ res_V_data_14_V int 16 regular {axi_s 1 volatile  { res_V_data_14_V Data } }  }
	{ res_V_data_15_V int 16 regular {axi_s 1 volatile  { res_V_data_15_V Data } }  }
}
set C_modelArgMapList {[ 
	{ "Name" : "data_V_data_0_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_1_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_2_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_3_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_4_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_5_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_6_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_7_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_8_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_9_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_10_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_11_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_12_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_13_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_14_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "data_V_data_15_V", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "res_V_data_0_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_1_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_2_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_3_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_4_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_5_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_6_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_7_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_8_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_9_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_10_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_11_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_12_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_13_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_14_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "res_V_data_15_V", "interface" : "axis", "bitwidth" : 16, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 103
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_continue sc_in sc_logic 1 continue -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ data_V_data_0_V_dout sc_in sc_lv 16 signal 0 } 
	{ data_V_data_0_V_empty_n sc_in sc_logic 1 signal 0 } 
	{ data_V_data_0_V_read sc_out sc_logic 1 signal 0 } 
	{ data_V_data_1_V_dout sc_in sc_lv 16 signal 1 } 
	{ data_V_data_1_V_empty_n sc_in sc_logic 1 signal 1 } 
	{ data_V_data_1_V_read sc_out sc_logic 1 signal 1 } 
	{ data_V_data_2_V_dout sc_in sc_lv 16 signal 2 } 
	{ data_V_data_2_V_empty_n sc_in sc_logic 1 signal 2 } 
	{ data_V_data_2_V_read sc_out sc_logic 1 signal 2 } 
	{ data_V_data_3_V_dout sc_in sc_lv 16 signal 3 } 
	{ data_V_data_3_V_empty_n sc_in sc_logic 1 signal 3 } 
	{ data_V_data_3_V_read sc_out sc_logic 1 signal 3 } 
	{ data_V_data_4_V_dout sc_in sc_lv 16 signal 4 } 
	{ data_V_data_4_V_empty_n sc_in sc_logic 1 signal 4 } 
	{ data_V_data_4_V_read sc_out sc_logic 1 signal 4 } 
	{ data_V_data_5_V_dout sc_in sc_lv 16 signal 5 } 
	{ data_V_data_5_V_empty_n sc_in sc_logic 1 signal 5 } 
	{ data_V_data_5_V_read sc_out sc_logic 1 signal 5 } 
	{ data_V_data_6_V_dout sc_in sc_lv 16 signal 6 } 
	{ data_V_data_6_V_empty_n sc_in sc_logic 1 signal 6 } 
	{ data_V_data_6_V_read sc_out sc_logic 1 signal 6 } 
	{ data_V_data_7_V_dout sc_in sc_lv 16 signal 7 } 
	{ data_V_data_7_V_empty_n sc_in sc_logic 1 signal 7 } 
	{ data_V_data_7_V_read sc_out sc_logic 1 signal 7 } 
	{ data_V_data_8_V_dout sc_in sc_lv 16 signal 8 } 
	{ data_V_data_8_V_empty_n sc_in sc_logic 1 signal 8 } 
	{ data_V_data_8_V_read sc_out sc_logic 1 signal 8 } 
	{ data_V_data_9_V_dout sc_in sc_lv 16 signal 9 } 
	{ data_V_data_9_V_empty_n sc_in sc_logic 1 signal 9 } 
	{ data_V_data_9_V_read sc_out sc_logic 1 signal 9 } 
	{ data_V_data_10_V_dout sc_in sc_lv 16 signal 10 } 
	{ data_V_data_10_V_empty_n sc_in sc_logic 1 signal 10 } 
	{ data_V_data_10_V_read sc_out sc_logic 1 signal 10 } 
	{ data_V_data_11_V_dout sc_in sc_lv 16 signal 11 } 
	{ data_V_data_11_V_empty_n sc_in sc_logic 1 signal 11 } 
	{ data_V_data_11_V_read sc_out sc_logic 1 signal 11 } 
	{ data_V_data_12_V_dout sc_in sc_lv 16 signal 12 } 
	{ data_V_data_12_V_empty_n sc_in sc_logic 1 signal 12 } 
	{ data_V_data_12_V_read sc_out sc_logic 1 signal 12 } 
	{ data_V_data_13_V_dout sc_in sc_lv 16 signal 13 } 
	{ data_V_data_13_V_empty_n sc_in sc_logic 1 signal 13 } 
	{ data_V_data_13_V_read sc_out sc_logic 1 signal 13 } 
	{ data_V_data_14_V_dout sc_in sc_lv 16 signal 14 } 
	{ data_V_data_14_V_empty_n sc_in sc_logic 1 signal 14 } 
	{ data_V_data_14_V_read sc_out sc_logic 1 signal 14 } 
	{ data_V_data_15_V_dout sc_in sc_lv 16 signal 15 } 
	{ data_V_data_15_V_empty_n sc_in sc_logic 1 signal 15 } 
	{ data_V_data_15_V_read sc_out sc_logic 1 signal 15 } 
	{ res_V_data_0_V_TREADY sc_in sc_logic 1 outacc 16 } 
	{ res_V_data_0_V_TDATA sc_out sc_lv 16 signal 16 } 
	{ res_V_data_0_V_TVALID sc_out sc_logic 1 outvld 16 } 
	{ res_V_data_1_V_TDATA sc_out sc_lv 16 signal 17 } 
	{ res_V_data_1_V_TVALID sc_out sc_logic 1 outvld 17 } 
	{ res_V_data_1_V_TREADY sc_in sc_logic 1 outacc 17 } 
	{ res_V_data_2_V_TDATA sc_out sc_lv 16 signal 18 } 
	{ res_V_data_2_V_TVALID sc_out sc_logic 1 outvld 18 } 
	{ res_V_data_2_V_TREADY sc_in sc_logic 1 outacc 18 } 
	{ res_V_data_3_V_TDATA sc_out sc_lv 16 signal 19 } 
	{ res_V_data_3_V_TVALID sc_out sc_logic 1 outvld 19 } 
	{ res_V_data_3_V_TREADY sc_in sc_logic 1 outacc 19 } 
	{ res_V_data_4_V_TDATA sc_out sc_lv 16 signal 20 } 
	{ res_V_data_4_V_TVALID sc_out sc_logic 1 outvld 20 } 
	{ res_V_data_4_V_TREADY sc_in sc_logic 1 outacc 20 } 
	{ res_V_data_5_V_TDATA sc_out sc_lv 16 signal 21 } 
	{ res_V_data_5_V_TVALID sc_out sc_logic 1 outvld 21 } 
	{ res_V_data_5_V_TREADY sc_in sc_logic 1 outacc 21 } 
	{ res_V_data_6_V_TDATA sc_out sc_lv 16 signal 22 } 
	{ res_V_data_6_V_TVALID sc_out sc_logic 1 outvld 22 } 
	{ res_V_data_6_V_TREADY sc_in sc_logic 1 outacc 22 } 
	{ res_V_data_7_V_TDATA sc_out sc_lv 16 signal 23 } 
	{ res_V_data_7_V_TVALID sc_out sc_logic 1 outvld 23 } 
	{ res_V_data_7_V_TREADY sc_in sc_logic 1 outacc 23 } 
	{ res_V_data_8_V_TDATA sc_out sc_lv 16 signal 24 } 
	{ res_V_data_8_V_TVALID sc_out sc_logic 1 outvld 24 } 
	{ res_V_data_8_V_TREADY sc_in sc_logic 1 outacc 24 } 
	{ res_V_data_9_V_TDATA sc_out sc_lv 16 signal 25 } 
	{ res_V_data_9_V_TVALID sc_out sc_logic 1 outvld 25 } 
	{ res_V_data_9_V_TREADY sc_in sc_logic 1 outacc 25 } 
	{ res_V_data_10_V_TDATA sc_out sc_lv 16 signal 26 } 
	{ res_V_data_10_V_TVALID sc_out sc_logic 1 outvld 26 } 
	{ res_V_data_10_V_TREADY sc_in sc_logic 1 outacc 26 } 
	{ res_V_data_11_V_TDATA sc_out sc_lv 16 signal 27 } 
	{ res_V_data_11_V_TVALID sc_out sc_logic 1 outvld 27 } 
	{ res_V_data_11_V_TREADY sc_in sc_logic 1 outacc 27 } 
	{ res_V_data_12_V_TDATA sc_out sc_lv 16 signal 28 } 
	{ res_V_data_12_V_TVALID sc_out sc_logic 1 outvld 28 } 
	{ res_V_data_12_V_TREADY sc_in sc_logic 1 outacc 28 } 
	{ res_V_data_13_V_TDATA sc_out sc_lv 16 signal 29 } 
	{ res_V_data_13_V_TVALID sc_out sc_logic 1 outvld 29 } 
	{ res_V_data_13_V_TREADY sc_in sc_logic 1 outacc 29 } 
	{ res_V_data_14_V_TDATA sc_out sc_lv 16 signal 30 } 
	{ res_V_data_14_V_TVALID sc_out sc_logic 1 outvld 30 } 
	{ res_V_data_14_V_TREADY sc_in sc_logic 1 outacc 30 } 
	{ res_V_data_15_V_TDATA sc_out sc_lv 16 signal 31 } 
	{ res_V_data_15_V_TVALID sc_out sc_logic 1 outvld 31 } 
	{ res_V_data_15_V_TREADY sc_in sc_logic 1 outacc 31 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_continue", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "continue", "bundle":{"name": "ap_continue", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "data_V_data_0_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_0_V", "role": "dout" }} , 
 	{ "name": "data_V_data_0_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_0_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_0_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_0_V", "role": "read" }} , 
 	{ "name": "data_V_data_1_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_1_V", "role": "dout" }} , 
 	{ "name": "data_V_data_1_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_1_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_1_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_1_V", "role": "read" }} , 
 	{ "name": "data_V_data_2_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_2_V", "role": "dout" }} , 
 	{ "name": "data_V_data_2_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_2_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_2_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_2_V", "role": "read" }} , 
 	{ "name": "data_V_data_3_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_3_V", "role": "dout" }} , 
 	{ "name": "data_V_data_3_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_3_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_3_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_3_V", "role": "read" }} , 
 	{ "name": "data_V_data_4_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_4_V", "role": "dout" }} , 
 	{ "name": "data_V_data_4_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_4_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_4_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_4_V", "role": "read" }} , 
 	{ "name": "data_V_data_5_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_5_V", "role": "dout" }} , 
 	{ "name": "data_V_data_5_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_5_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_5_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_5_V", "role": "read" }} , 
 	{ "name": "data_V_data_6_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_6_V", "role": "dout" }} , 
 	{ "name": "data_V_data_6_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_6_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_6_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_6_V", "role": "read" }} , 
 	{ "name": "data_V_data_7_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_7_V", "role": "dout" }} , 
 	{ "name": "data_V_data_7_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_7_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_7_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_7_V", "role": "read" }} , 
 	{ "name": "data_V_data_8_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_8_V", "role": "dout" }} , 
 	{ "name": "data_V_data_8_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_8_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_8_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_8_V", "role": "read" }} , 
 	{ "name": "data_V_data_9_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_9_V", "role": "dout" }} , 
 	{ "name": "data_V_data_9_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_9_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_9_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_9_V", "role": "read" }} , 
 	{ "name": "data_V_data_10_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_10_V", "role": "dout" }} , 
 	{ "name": "data_V_data_10_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_10_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_10_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_10_V", "role": "read" }} , 
 	{ "name": "data_V_data_11_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_11_V", "role": "dout" }} , 
 	{ "name": "data_V_data_11_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_11_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_11_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_11_V", "role": "read" }} , 
 	{ "name": "data_V_data_12_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_12_V", "role": "dout" }} , 
 	{ "name": "data_V_data_12_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_12_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_12_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_12_V", "role": "read" }} , 
 	{ "name": "data_V_data_13_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_13_V", "role": "dout" }} , 
 	{ "name": "data_V_data_13_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_13_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_13_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_13_V", "role": "read" }} , 
 	{ "name": "data_V_data_14_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_14_V", "role": "dout" }} , 
 	{ "name": "data_V_data_14_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_14_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_14_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_14_V", "role": "read" }} , 
 	{ "name": "data_V_data_15_V_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "data_V_data_15_V", "role": "dout" }} , 
 	{ "name": "data_V_data_15_V_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_15_V", "role": "empty_n" }} , 
 	{ "name": "data_V_data_15_V_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "data_V_data_15_V", "role": "read" }} , 
 	{ "name": "res_V_data_0_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_0_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_0_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_0_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_0_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_0_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_1_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_1_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_1_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_1_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_1_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_1_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_2_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_2_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_2_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_2_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_2_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_2_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_3_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_3_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_3_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_3_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_3_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_3_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_4_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_4_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_4_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_4_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_4_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_4_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_5_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_5_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_5_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_5_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_5_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_5_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_6_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_6_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_6_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_6_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_6_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_6_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_7_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_7_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_7_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_7_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_7_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_7_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_8_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_8_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_8_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_8_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_8_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_8_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_9_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_9_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_9_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_9_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_9_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_9_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_10_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_10_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_10_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_10_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_10_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_10_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_11_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_11_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_11_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_11_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_11_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_11_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_12_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_12_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_12_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_12_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_12_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_12_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_13_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_13_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_13_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_13_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_13_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_13_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_14_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_14_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_14_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_14_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_14_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_14_V", "role": "TREADY" }} , 
 	{ "name": "res_V_data_15_V_TDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "res_V_data_15_V", "role": "TDATA" }} , 
 	{ "name": "res_V_data_15_V_TVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "res_V_data_15_V", "role": "TVALID" }} , 
 	{ "name": "res_V_data_15_V_TREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "outacc", "bundle":{"name": "res_V_data_15_V", "role": "TREADY" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"],
		"CDFG" : "relu_array_ap_fixed_16u_array_ap_ufixed_9_1_4_0_0_16u_relu_config9_s",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "Aligned", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "1",
		"VariableLatency" : "0", "ExactLatency" : "2", "EstimateLatencyMin" : "2", "EstimateLatencyMax" : "2",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "data_V_data_0_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_0_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_1_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_1_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_2_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_2_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_3_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_3_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_4_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_4_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_5_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_5_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_6_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_6_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_7_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_7_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_8_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_8_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_9_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_9_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_10_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_10_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_11_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_11_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_12_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_12_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_13_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_13_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_14_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_14_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "data_V_data_15_V", "Type" : "Fifo", "Direction" : "I", "DependentProc" : "0", "DependentChan" : "0",
				"BlockSignal" : [
					{"Name" : "data_V_data_15_V_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_0_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_0_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_1_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_1_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_2_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_2_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_3_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_3_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_4_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_4_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_5_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_5_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_6_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_6_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_7_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_7_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_8_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_8_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_9_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_9_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_10_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_10_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_11_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_11_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_12_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_12_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_13_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_13_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_14_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_14_V_TDATA_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "res_V_data_15_V", "Type" : "Axis", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "res_V_data_15_V_TDATA_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_0_V_U", "Parent" : "0"},
	{"ID" : "2", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_1_V_U", "Parent" : "0"},
	{"ID" : "3", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_2_V_U", "Parent" : "0"},
	{"ID" : "4", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_3_V_U", "Parent" : "0"},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_4_V_U", "Parent" : "0"},
	{"ID" : "6", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_5_V_U", "Parent" : "0"},
	{"ID" : "7", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_6_V_U", "Parent" : "0"},
	{"ID" : "8", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_7_V_U", "Parent" : "0"},
	{"ID" : "9", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_8_V_U", "Parent" : "0"},
	{"ID" : "10", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_9_V_U", "Parent" : "0"},
	{"ID" : "11", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_10_V_U", "Parent" : "0"},
	{"ID" : "12", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_11_V_U", "Parent" : "0"},
	{"ID" : "13", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_12_V_U", "Parent" : "0"},
	{"ID" : "14", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_13_V_U", "Parent" : "0"},
	{"ID" : "15", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_14_V_U", "Parent" : "0"},
	{"ID" : "16", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.regslice_both_res_V_data_15_V_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	relu_array_ap_fixed_16u_array_ap_ufixed_9_1_4_0_0_16u_relu_config9_s {
		data_V_data_0_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_1_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_2_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_3_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_4_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_5_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_6_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_7_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_8_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_9_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_10_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_11_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_12_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_13_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_14_V {Type I LastRead 0 FirstWrite -1}
		data_V_data_15_V {Type I LastRead 0 FirstWrite -1}
		res_V_data_0_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_1_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_2_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_3_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_4_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_5_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_6_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_7_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_8_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_9_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_10_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_11_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_12_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_13_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_14_V {Type O LastRead -1 FirstWrite 1}
		res_V_data_15_V {Type O LastRead -1 FirstWrite 1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "2", "Max" : "2"}
	, {"Name" : "Interval", "Min" : "1", "Max" : "1"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	data_V_data_0_V { ap_fifo {  { data_V_data_0_V_dout fifo_data 0 16 }  { data_V_data_0_V_empty_n fifo_status 0 1 }  { data_V_data_0_V_read fifo_update 1 1 } } }
	data_V_data_1_V { ap_fifo {  { data_V_data_1_V_dout fifo_data 0 16 }  { data_V_data_1_V_empty_n fifo_status 0 1 }  { data_V_data_1_V_read fifo_update 1 1 } } }
	data_V_data_2_V { ap_fifo {  { data_V_data_2_V_dout fifo_data 0 16 }  { data_V_data_2_V_empty_n fifo_status 0 1 }  { data_V_data_2_V_read fifo_update 1 1 } } }
	data_V_data_3_V { ap_fifo {  { data_V_data_3_V_dout fifo_data 0 16 }  { data_V_data_3_V_empty_n fifo_status 0 1 }  { data_V_data_3_V_read fifo_update 1 1 } } }
	data_V_data_4_V { ap_fifo {  { data_V_data_4_V_dout fifo_data 0 16 }  { data_V_data_4_V_empty_n fifo_status 0 1 }  { data_V_data_4_V_read fifo_update 1 1 } } }
	data_V_data_5_V { ap_fifo {  { data_V_data_5_V_dout fifo_data 0 16 }  { data_V_data_5_V_empty_n fifo_status 0 1 }  { data_V_data_5_V_read fifo_update 1 1 } } }
	data_V_data_6_V { ap_fifo {  { data_V_data_6_V_dout fifo_data 0 16 }  { data_V_data_6_V_empty_n fifo_status 0 1 }  { data_V_data_6_V_read fifo_update 1 1 } } }
	data_V_data_7_V { ap_fifo {  { data_V_data_7_V_dout fifo_data 0 16 }  { data_V_data_7_V_empty_n fifo_status 0 1 }  { data_V_data_7_V_read fifo_update 1 1 } } }
	data_V_data_8_V { ap_fifo {  { data_V_data_8_V_dout fifo_data 0 16 }  { data_V_data_8_V_empty_n fifo_status 0 1 }  { data_V_data_8_V_read fifo_update 1 1 } } }
	data_V_data_9_V { ap_fifo {  { data_V_data_9_V_dout fifo_data 0 16 }  { data_V_data_9_V_empty_n fifo_status 0 1 }  { data_V_data_9_V_read fifo_update 1 1 } } }
	data_V_data_10_V { ap_fifo {  { data_V_data_10_V_dout fifo_data 0 16 }  { data_V_data_10_V_empty_n fifo_status 0 1 }  { data_V_data_10_V_read fifo_update 1 1 } } }
	data_V_data_11_V { ap_fifo {  { data_V_data_11_V_dout fifo_data 0 16 }  { data_V_data_11_V_empty_n fifo_status 0 1 }  { data_V_data_11_V_read fifo_update 1 1 } } }
	data_V_data_12_V { ap_fifo {  { data_V_data_12_V_dout fifo_data 0 16 }  { data_V_data_12_V_empty_n fifo_status 0 1 }  { data_V_data_12_V_read fifo_update 1 1 } } }
	data_V_data_13_V { ap_fifo {  { data_V_data_13_V_dout fifo_data 0 16 }  { data_V_data_13_V_empty_n fifo_status 0 1 }  { data_V_data_13_V_read fifo_update 1 1 } } }
	data_V_data_14_V { ap_fifo {  { data_V_data_14_V_dout fifo_data 0 16 }  { data_V_data_14_V_empty_n fifo_status 0 1 }  { data_V_data_14_V_read fifo_update 1 1 } } }
	data_V_data_15_V { ap_fifo {  { data_V_data_15_V_dout fifo_data 0 16 }  { data_V_data_15_V_empty_n fifo_status 0 1 }  { data_V_data_15_V_read fifo_update 1 1 } } }
	res_V_data_0_V { axis {  { res_V_data_0_V_TREADY out_acc 0 1 }  { res_V_data_0_V_TDATA out_data 1 16 }  { res_V_data_0_V_TVALID out_vld 1 1 } } }
	res_V_data_1_V { axis {  { res_V_data_1_V_TDATA out_data 1 16 }  { res_V_data_1_V_TVALID out_vld 1 1 }  { res_V_data_1_V_TREADY out_acc 0 1 } } }
	res_V_data_2_V { axis {  { res_V_data_2_V_TDATA out_data 1 16 }  { res_V_data_2_V_TVALID out_vld 1 1 }  { res_V_data_2_V_TREADY out_acc 0 1 } } }
	res_V_data_3_V { axis {  { res_V_data_3_V_TDATA out_data 1 16 }  { res_V_data_3_V_TVALID out_vld 1 1 }  { res_V_data_3_V_TREADY out_acc 0 1 } } }
	res_V_data_4_V { axis {  { res_V_data_4_V_TDATA out_data 1 16 }  { res_V_data_4_V_TVALID out_vld 1 1 }  { res_V_data_4_V_TREADY out_acc 0 1 } } }
	res_V_data_5_V { axis {  { res_V_data_5_V_TDATA out_data 1 16 }  { res_V_data_5_V_TVALID out_vld 1 1 }  { res_V_data_5_V_TREADY out_acc 0 1 } } }
	res_V_data_6_V { axis {  { res_V_data_6_V_TDATA out_data 1 16 }  { res_V_data_6_V_TVALID out_vld 1 1 }  { res_V_data_6_V_TREADY out_acc 0 1 } } }
	res_V_data_7_V { axis {  { res_V_data_7_V_TDATA out_data 1 16 }  { res_V_data_7_V_TVALID out_vld 1 1 }  { res_V_data_7_V_TREADY out_acc 0 1 } } }
	res_V_data_8_V { axis {  { res_V_data_8_V_TDATA out_data 1 16 }  { res_V_data_8_V_TVALID out_vld 1 1 }  { res_V_data_8_V_TREADY out_acc 0 1 } } }
	res_V_data_9_V { axis {  { res_V_data_9_V_TDATA out_data 1 16 }  { res_V_data_9_V_TVALID out_vld 1 1 }  { res_V_data_9_V_TREADY out_acc 0 1 } } }
	res_V_data_10_V { axis {  { res_V_data_10_V_TDATA out_data 1 16 }  { res_V_data_10_V_TVALID out_vld 1 1 }  { res_V_data_10_V_TREADY out_acc 0 1 } } }
	res_V_data_11_V { axis {  { res_V_data_11_V_TDATA out_data 1 16 }  { res_V_data_11_V_TVALID out_vld 1 1 }  { res_V_data_11_V_TREADY out_acc 0 1 } } }
	res_V_data_12_V { axis {  { res_V_data_12_V_TDATA out_data 1 16 }  { res_V_data_12_V_TVALID out_vld 1 1 }  { res_V_data_12_V_TREADY out_acc 0 1 } } }
	res_V_data_13_V { axis {  { res_V_data_13_V_TDATA out_data 1 16 }  { res_V_data_13_V_TVALID out_vld 1 1 }  { res_V_data_13_V_TREADY out_acc 0 1 } } }
	res_V_data_14_V { axis {  { res_V_data_14_V_TDATA out_data 1 16 }  { res_V_data_14_V_TVALID out_vld 1 1 }  { res_V_data_14_V_TREADY out_acc 0 1 } } }
	res_V_data_15_V { axis {  { res_V_data_15_V_TDATA out_data 1 16 }  { res_V_data_15_V_TVALID out_vld 1 1 }  { res_V_data_15_V_TREADY out_acc 0 1 } } }
}
