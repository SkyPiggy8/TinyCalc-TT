# TinyCalc-TT — Yellow Mascot VGA ASIC

Tiny Tapeout SKY130 Verilog project displaying a simplified pixel-art interpretation of the supplied yellow character on a VGA monitor.

**This is a first working RTL draft, not yet a verified GDS/tapeout-ready design.** The original reference image has not been converted to an exact ROM sprite; this implementation draws a compact procedural approximation to keep silicon usage low.

## Official Tiny Tapeout layout

- `info.yaml`: project, pinout, tiles and top-module metadata
- `src/project.v`: synthesizable VGA timing and character renderer
- `test/test.py` and `test/tb.v`: Cocotb interface checks
- `docs/info.md`: operation, clock, connection and verification notes
- `.github/workflows/`: Tiny Tapeout GDS, docs and simulation checks

## Video
- 640x480, nominal 59.94 Hz, 25.175 MHz pixel clock provided externally
- TinyVGA PMOD output with 2 bits per R/G/B channel
- Fixed yellow mascot on white background
- No CPU, frame buffer or external RAM

## Status
Workflows must pass before submitting to https://app.tinytapeout.com/projects/create . Selected tile size `1x2` is an estimate, **not validated** by place/route or precheck.

Previous calculator RTL and physical layout are retained elsewhere in the repository as historical experiments; they are **not** the active Tiny Tapeout design.

Source template: https://github.com/TinyTapeout/ttsky-verilog-template
