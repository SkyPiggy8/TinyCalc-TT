# Yellow Mascot VGA Display

## How it works

The chip generates standard 640x480 VGA timing using a 25.175 MHz input pixel clock. The renderer produces a small, stylized yellow creature with green eyes, cream belly and brown hands/feet. It is a procedural approximation, not an exact photographic bitmap. All pixels are generated using comparisons (no external ROM).

## Pinout

- `uo_out[0]`: R1; `uo_out[4]`: R0
- `uo_out[1]`: G1; `uo_out[5]`: G0
- `uo_out[2]`: B1; `uo_out[6]`: B0
- `uo_out[3]`: VSYNC, `uo_out[7]`: HSYNC
- `clk`: external pixel clock at 25.175 MHz, `rst_n`: active-low reset, `ena`: timing enable
- `ui_in`, `uio_in`: unused; all bidirectional pins are high impedance

## How to test

Use Cocotb in `test/` with Icarus Verilog, then inspect the GitHub GDS and precheck jobs. Connect the ASIC demo board to a TinyVGA PMOD and compatible VGA monitor. The VGA outputs are digital and require a suitable resistor DAC; they must not connect directly to analog VGA pins.

## Limitations

RTL, GDS/DRC/LVS, timing closure and exact artwork fidelity must be checked independently. Successful push to GitHub is not a manufacturing approval.
