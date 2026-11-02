// SPDX-License-Identifier: Apache-2.0
// Unsigned 8-bit operands, 16-bit result; one shared adder.
`default_nettype none
module tt_um_skypiggy8_tinycalc (
 input wire [7:0] ui_in, output wire [7:0] uo_out,
 input wire [7:0] uio_in, output wire [7:0] uio_out, uio_oe,
 input wire ena, clk, rst_n
);
 reg [15:0] acc;
 reg [7:0] rhs, count;
 reg divide, busy, divzero;
 wire subtract = busy ? divide : uio_in[3];
 wire [15:0] operand = {8'b0, rhs};
 wire [16:0] sum = {1'b0, acc} + {1'b0, (operand ^ {16{subtract}})} + {16'b0, subtract};
 wire ge_rhs = sum[16];
 always @(posedge clk) begin
  if (!rst_n) begin
   acc<=0; rhs<=0; count<=0; divide<=0; busy<=0; divzero<=0;
  end else if (ena) begin
   if (busy) begin
    if (divide) begin
     if (ge_rhs) begin acc<=sum[15:0]; count<=count+1'b1; end
     else begin acc<={8'b0,count}; busy<=0; end
    end else begin
     acc<=sum[15:0]; count<=count-1'b1;
     if(count==1) busy<=0;
    end
   end else if(uio_in[0]) begin acc<={8'b0,ui_in}; divzero<=0; end
   else if(uio_in[1]) rhs<=ui_in;
   else if(uio_in[2]) begin
    divzero<=0;
    case(uio_in[4:3])
     2'b00,2'b01: acc<=sum[15:0];
     2'b10: begin count<=acc[7:0]; acc<=0; divide<=0; busy<=|acc[7:0]; end
     2'b11: begin
      count<=0; divide<=1;
      if(rhs==0) begin acc<=16'hffff; divzero<=1; end
      else busy<=1;
     end
    endcase
   end
  end
 end
 assign uo_out=uio_in[5]?acc[15:8]:acc[7:0];
 assign uio_out={divzero,busy,6'b0};
 assign uio_oe=8'b11000000;
 wire _unused=&{uio_in[7:6],1'b0};
endmodule
`default_nettype wire
