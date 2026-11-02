# Dual-function Tiny Tapeout ASIC: VGA + 8-bit calculator

## VGA
640x480 / 25.175 MHz external pixel clock. Fixed geometric mascot graphic on uo_out through a TinyVGA PMOD. VGA runs **at the same time as the calculator**; it is not a selectable exclusive mode.

## Calculator
Unsigned 8-bit operands A and B; 16-bit result. Add/subtract/multiply/divide, with repeated addition/subtraction to avoid dedicated multipliers/dividers.

1. With rst_n low for at least one rising edge, reset the chip; then release reset and keep ena high.
2. Set ui_in to A; pulse uio_in[0]=1 for one clock.
3. Set ui_in to B; pulse uio_in[1]=1 for one clock.
4. Put OP in uio_in[4:3]: 00 add, 01 subtract, 10 multiply, 11 integer divide. Pulse uio_in[2]=1 for one clock.
5. With ui_in[7]=0, read uio_out[6]=BUSY and [7]=DIVZERO; wait for BUSY=0.
6. Result readback has two banks. Choose low/high result byte with uio_in[5]. Read uio_out[5:0] as the lower six bits of that byte. To read the top two bits, set ui_in[7]=1 and take uio_out[7:6]. Then restore ui_in[7]=0 to see status.
7. All uio pins are outputs when reading; the Tiny Tapeout host must safely drive command pins only if the I/O interface supports bidirectional handling. **The host and chip must never drive the same pin at the same time.**

## Important electrical limitation
The minimal dual-function prototype reuses each uio pin as both a command input and a result output but sets uio_oe=0xff. That makes simultaneous external host driving unsafe on a standard board. This is an **experimental architecture**, not a safe final electrical interface. An external controller must not actively drive those pins until an input/output turnaround scheme has been implemented. The design requires an I/O redesign before hardware connection or tapeout submission.

## Physical status
1x1 is an exploratory target. The project must pass synth/place/route/GDS and precheck; no area or timing fit is claimed.
