// SPDX-License-Identifier: Apache-2.0
`default_nettype none
// 640x480 @ 25.175 MHz, TinyVGA PMOD. Procedural mascot illustration.
module tt_um_skypiggy8_nailong(
 input wire [7:0] ui_in, output wire [7:0] uo_out,
 input wire [7:0] uio_in, output wire [7:0] uio_out,
 output wire [7:0] uio_oe, input wire ena, clk, rst_n
);
 // Calculator: ui_in is an 8-bit operand on LOAD pulses.
 // uio_in[0] LOAD_A, [1] LOAD_B, [2] START, [4:3] OP.
 // uio_out[6] BUSY, [7] serial data bit; uio_oe=8'b11000000.
 // Read result via ui_in[3]=0, ui_in[4] byte, ui_in[2:0] bit-index.
 // Read DIVZERO via ui_in[3]=1 (on uio_out[7]).
 reg [15:0] acc;
 reg [7:0] rhs, count;
 reg divide, busy, divzero;
 wire sub = busy ? divide : uio_in[3];
 wire [15:0] oper = {8'b0,rhs};
 wire [16:0] sum = {1'b0,acc} + {1'b0,(oper ^ {16{sub}})} + {16'b0,sub};
 always @(posedge clk) begin
  if (!rst_n) begin
   acc<=0; rhs<=0; count<=0; divide<=0; busy<=0; divzero<=0;
  end else if(ena) begin
   if(busy) begin
    if(divide) begin
     if(sum[16]) begin acc<=sum[15:0]; count<=count+1'b1; end
     else begin acc<={8'b0,count};busy<=0;end
    end else begin
     acc<=sum[15:0];count<=count-1'b1;
     if(count==1) busy<=0;
    end
   end else if(uio_in[0]) begin acc<={8'b0,ui_in};divzero<=0;end
   else if(uio_in[1]) rhs<=ui_in;
   else if(uio_in[2]) begin
    divzero<=0;
    case(uio_in[4:3])
     2'b00,2'b01: acc<=sum[15:0];
     2'b10: begin count<=acc[7:0];acc<=0;divide<=0;busy<=|acc[7:0];end
     2'b11: begin
       count<=0;divide<=1;
       if(rhs==0) begin acc<=16'hffff;divzero<=1;end
       else busy<=1;
     end
    endcase
   end
  end
 end
 wire [7:0] result_byte = ui_in[4] ? acc[15:8] : acc[7:0];
 wire serial_data = ui_in[3] ? divzero : result_byte[ui_in[2:0]];
 reg [9:0] x, y;
 always @(posedge clk) begin
  if (!rst_n) begin x <= 0; y <= 0; end
  else if (ena) begin
   if (x == 799) begin
    x <= 0;
    if (y == 524) y <= 0;
    else y <= y + 1'b1;
   end else x <= x + 1'b1;
  end
 end
 wire visible = (x < 640 && y < 480);
 wire hs = !(x >= 656 && x < 752);
 wire vs = !(y >= 490 && y < 492);
 // Stair-step curves intentionally use comparisons rather than large image ROM.
 reg [9:0] left_edge, right_edge;
 always @* begin
  left_edge = 320; right_edge = 320;
  if (y>=73 && y<105) begin left_edge=291; right_edge=369; end
  else if (y>=105 && y<145) begin left_edge=276; right_edge=392; end
  else if (y>=145 && y<190) begin left_edge=283; right_edge=408; end
  else if (y>=190 && y<240) begin left_edge=258; right_edge=430; end
  else if (y>=240 && y<310) begin left_edge=228; right_edge=442; end
  else if (y>=310 && y<360) begin left_edge=237; right_edge=438; end
  else if (y>=360 && y<390) begin left_edge=260; right_edge=419; end
 end
 wire body = (x>=left_edge && x<=right_edge && y>=73 && y<390);
 wire belly = (y>=219 && y<350 && x>=274 && x<=397) ||
              (y>=195 && y<219 && x>=292 && x<=380) ||
              (y>=350 && y<363 && x>=298 && x<=375);
 wire leg_l = (y>=380 && y<440 && x>=280 && x<326);
 wire leg_r = (y>=380 && y<440 && x>=353 && x<400);
 wire foot_l = (y>=431 && y<447 && x>=265 && x<335);
 wire foot_r = (y>=431 && y<447 && x>=346 && x<411);
 wire arm_l = (y>=272 && y<325 && x>=239 && x<283);
 wire arm_r = (y>=265 && y<316 && x>=385 && x<429);
 wire hand_l = (y>=301 && y<335 && x>=263 && x<287);
 wire hand_r = (y>=294 && y<328 && x>=374 && x<401);
 wire eye_outer = (y>=117 && y<147 && x>=298 && x<330) ||
                  (y>=105 && y<140 && x>=356 && x<388);
 wire eye_inner = (y>=123 && y<143 && x>=307 && x<325) ||
                  (y>=112 && y<135 && x>=364 && x<383);
 wire mouth = (y>=165 && y<168 && x>=294 && x<332);
 reg [5:0] rgb;
 always @* begin
  rgb=6'b111111; // white
  if (body || leg_l || leg_r || arm_l || arm_r) rgb=6'b110000; // yellow (R=3,G=0,B=0) overwritten below
  if (body || leg_l || leg_r || arm_l || arm_r) rgb=6'b111100; // bright yellow R=3 G=3 B=0
  if (belly && body) rgb=6'b111001; // pale cream
  if (foot_l || foot_r || hand_l || hand_r) rgb=6'b010100; // brown
  if (eye_outer) rgb=6'b001100; // green
  if (eye_inner || mouth) rgb=6'b000000; // black
  if (!visible) rgb=6'b000000;
 end
 // RGB bits ordered {R[1:0], G[1:0], B[1:0]}.
 assign uo_out={hs,rgb[0],rgb[2],rgb[4],vs,rgb[1],rgb[3],rgb[5]};
 assign uio_out={serial_data,busy,6'b0};
 assign uio_oe=8'b11000000;
 wire _unused=&{uio_in[7:5],1'b0};
endmodule
`default_nettype wire
