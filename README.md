# TinyCalc-TT — Nai Wa VGA + 8-bit Calculator

Experimental dual-function Tiny Tapeout SKY130 ASIC: generate a yellow-mascot VGA picture **and** calculate 8-bit addition, subtraction, multiplication, and integer division in parallel.

- VGA: fixed procedural drawing on `uo_out[7:0]`, nominal 640x480 @ 25.175 MHz via TinyVGA PMOD.
- Calculator: 8-bit inputs, 16-bit outputs, shared sequential adder. `ui_in` takes operands; `uio[5:0]` receive control inputs; `uio[6:7]` output BUSY and serialized result/DIVZERO.
- The two features operate **at the same time**, with no VGA / calculator mode switching required.
- `info.yaml` is configured for a **trial `1x1` tile**, not an independently proven physical fit.

**Not tapeout-ready:** RTL has been uploaded but no confirmed placement/routing, area, timing, DRC/LVS or Tiny Tapeout precheck pass is available. The mascot uses simplified geometry, **not** an exact reproduction of the user's source image.

See [docs/info.md](docs/info.md) for the complete pinout and step-by-step use. Standard Tiny Tapeout structure: `info.yaml`, `src/project.v`, `test/`, `docs/`, `.github/workflows/`.

Template: https://github.com/TinyTapeout/ttsky-verilog-template
