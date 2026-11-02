# TinyCalc-TT — Calculator + Yellow Mascot VGA

Experimental SKY130 Tiny Tapeout **two-function ASIC**. A simple yellow mascot VGA picture is generated continuously, while a sequential 8-bit arithmetic engine calculates addition, subtraction, multiplication and unsigned division.

## What is implemented
- VGA timing for 640x480 @ 25.175 MHz and a **procedural approximation**, not an exact bitmap, of the supplied yellow character
- Unsigned 8-bit operands, 16-bit result
- Four arithmetic functions, using a shared add/subtract datapath
- Tiny Tapeout standard `src/project.v`, `info.yaml`, `test/`, `docs/`, `.github/workflows/`

## Status: not ready for manufacturing
The design has been combined and pushed for testing with **1x1 tile as an experimental area target**. The selected tile size is **not yet verified to fit** and the existing calculator input/output sharing scheme has an **electrical bus contention issue** (see [docs/info.md](docs/info.md)). Do not connect control signals to physical uio pins until the interface is redesigned and tested.

The exact user image is not yet reproduced. This early design uses shapes and colors rather than a detailed pixel ROM.

See [docs/info.md](docs/info.md) for logic behavior and limitations. See the official [Tiny Tapeout Verilog template](https://github.com/TinyTapeout/ttsky-verilog-template).
