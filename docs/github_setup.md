# GitHub / Tiny Tapeout build setup

Intended repository: `SkyPiggy8/TinyCalc-TT`.

## Repository root

Upload the CONTENTS of the project folder to the repository root, not a ZIP file
and not a second nested `TinyCalc-TT` directory. `info.yaml`, `src`, `test`, `docs`
and `.github/workflows` must be directly under the repository root.

If creating the repository manually, create an empty repository at
https://github.com/new with name `TinyCalc-TT`. Do not initialize another README,
license or gitignore. This project already includes the official template's
Apache-2.0 license, git history and workflow files.

## Official template retained

Template: https://github.com/TinyTapeout/ttsky-verilog-template

Template source commit: `a42e6662fab316e93b4e26399e21d41664a460b7`.
See `reports/template_check.txt` for the local validation record.

| Path | Role |
| --- | --- |
| `info.yaml` | YAML v6 metadata, tile target, top module, source files, pinout |
| `src/project.v` | `tt_um_skypiggy8_tinycalc`, official eight-port wrapper |
| `src/config.json` | LibreLane settings; requested 100 kHz clock |
| `test/Makefile`, `test/tb.v`, `test/test.py` | Cocotb RTL / gate-level tests |
| `docs/info.md` | Project datasheet / interface usage |
| `.github/workflows/gds.yaml` | Official SKY26d GDS, precheck, gate-level test, viewer |
| `.github/workflows/docs.yaml` | Official project documentation build |
| `.github/workflows/test.yaml` | Cocotb RTL tests |
| `.github/workflows/exhaustive.yaml` | Additional exhaustive generic-gate tests |
| `.github/workflows/fpga.yaml` | Optional manual FPGA simulator build |

## First online build

1. Open the repository's Actions tab and allow workflows if GitHub asks.
2. Push to `main`; `gds`, `docs`, `test` and exhaustive verification run.
3. For the viewer, set Settings > Pages > Source to GitHub Actions.
4. Inspect all jobs and download their artifacts. A viewer/Pages failure is
   separate from a failed GDS generation or precheck job.
5. Do not submit for fabrication until GDS, precheck and gate-level tests pass.

The automatic reference GDS is generated from `src/project.v`. It does not use
the manual `layout/calculator_placement_ONLY.gds` file as a finished macro.
The experimental manual layout has its own incomplete status in
`docs/physical_status.md`; successful automatic generation does not validate it.

Repository creation, upload and online workflow results must be checked
separately; local validation alone is not evidence of a successful upload.
