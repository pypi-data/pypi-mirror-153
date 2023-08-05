import dm::*;

module dm_wrap (
    // Common
    input  logic clk,
    input  logic rst_n,
    // CPU
    output logic ndmreset,
    output logic debug_req,

    // CPU -> DM
    input  logic dm_req,
    input  logic dm_we,
    input  logic [31:0] dm_addr,
    input  logic [3:0] dm_be,
    input  logic [31:0] dm_wdata,
    output logic [31:0] dm_rdata,

    // DM -> system bus
    output logic sb_req,
    output logic [31:0] sb_addr,
    output logic sb_we,
    output logic [31:0] sb_wdata,
    output logic [3:0] sb_be,
    input  logic sb_gnt,
    input  logic sb_rvalid,
    input  logic [31:0] sb_rdata,

    // JTAG interface
    input  logic tck,
    input  logic tms,
    input  logic trst_n,
    input  logic tdi,
    output logic tdo,
    output logic tdo_oe
);

    logic debug_req_ready;
    dmi_resp_t debug_resp;
    logic jtag_req_valid;
    dmi_req_t jtag_dmi_req;
    logic jtag_resp_ready;
    logic jtag_resp_valid;

    dm_top #(
        .NrHarts(1),
        .BusWidth(32),
        .SelectableHarts(1)
    ) dm_top_i (
        .clk_i(clk),
        .rst_ni(rst_n),
        .testmode_i(0),
        .ndmreset_o(ndmreset),
        .debug_req_o(debug_req),
        .unavailable_i(0),
        .hartinfo_i('0),
        .slave_req_i(dm_req),
        .slave_we_i(dm_we),
        .slave_addr_i(dm_addr),
        .slave_be_i(dm_be),
        .slave_wdata_i(dm_wdata),
        .slave_rdata_o(dm_rdata),

        .master_req_o(sb_req),
        .master_add_o(sb_addr),
        .master_we_o(sb_we),
        .master_wdata_o(sb_wdata),
        .master_be_o(sb_be),
        .master_gnt_i(sb_gnt),
        .master_r_valid_i(sb_rvalid),
        .master_r_rdata_i(sb_rdata),

        .dmi_rst_ni(rst_n),
        .dmi_req_valid_i(jtag_req_valid),
        .dmi_req_ready_o(debug_req_ready),
        .dmi_req_i(jtag_dmi_req),
        .dmi_resp_valid_o(jtag_resp_valid),
        .dmi_resp_ready_i(jtag_resp_ready),
        .dmi_resp_o(debug_resp)
    );

    dmi_jtag #(
        .IdcodeValue(32'h249511C3)
    ) dmi_jtag_i (
        .clk_i(clk),
        .rst_ni(rst_n),
        .testmode_i(0),
        .dmi_req_o(jtag_dmi_req),
        .dmi_req_valid_o(jtag_req_valid),
        .dmi_req_ready_i(debug_req_ready),
        .dmi_resp_i(debug_resp),
        .dmi_resp_ready_o(jtag_resp_ready),
        .dmi_resp_valid_i(jtag_resp_valid),
        .tck_i(tck),
        .tms_i(tms),
        .trst_ni(trst_n),
        .td_i(tdi),
        .td_o(tdo),
        .tdo_oe_o(tdo_oe)
    );

endmodule : dm_wrap
