# TinyCalc + Nai Wa VGA: how to use

## Video output
VGA runs continuously at 640x480, nominal 59.94 Hz with an external 25.175 MHz pixel clock. `uo_out[0:7]` follow TinyVGA PMOD pin ordering: R1, G1, B1, VSync, R0, G0, B0, HSync. A simplified yellow mascot is drawn with comparator-based geometry; it is not a pixel-perfect version of the reference artwork.

## Calculator, simultaneously with VGA
Inputs `ui_in[7:0]` carry full 8-bit operand values during load operations. The five control inputs are `uio_in[0]` LOAD_A, `[1]` LOAD_B, `[2]` START, `[4:3]` OP (00 add, 01 subtract, 10 multiply, 11 unsigned integer divide). All controls are sampled on a rising pixel-clock edge when `ena=1`.

1. Reset with `rst_n=0` for at least one clock; release reset.
2. Drive operand A on `ui_in`, pulse LOAD_A once.
3. Drive operand B on `ui_in`, pulse LOAD_B once.
4. Set OP and pulse START once.
5. `uio_out[6]` is BUSY. Wait until 0. `uio_out[7]` is serial output.
6. Read result one bit at a time: `ui_in[3]=0`, `ui_in[4]=0` for low byte or `1` for high byte, `ui_in[2:0]` selects bit 0 to 7. Read selected bit from `uio_out[7]`, concatenate all 16 bits.
7. To read DIVZERO flag, set `ui_in[3]=1`, read `uio_out[7]`.

`uio_oe=8'b11000000` always: `uio[5:0]` are input-only; `uio[7:6]` are output-only. Never drive `uio[7:6]` externally. `ui_in[7:0]` values during read are only address/selection bits and do not alter operands unless a LOAD control is asserted.

The addition/subtraction result is 16-bit two's-complement for negative subtraction; division truncates; division by zero returns `0xffff` and flags DIVZERO. Multiply and divide take multiple clocks.

## Manufacturing status
The `1x1` SKY130 tile is an experimental target only. The implementation requires synthesis, timing analysis, physical routing, DRC/LVS and official Tiny Tapeout precheck before claiming tapeout readiness. Pixel-art fidelity to the supplied picture has not been established.
