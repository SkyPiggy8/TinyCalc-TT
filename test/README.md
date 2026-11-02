# TinyCalc testbench

This testbench uses [cocotb](https://docs.cocotb.org/en/stable/) to drive TinyCalc's synchronous operand/control interface and check arithmetic, divide-by-zero and I/O direction.
See below to get started or for more information, check the [website](https://tinytapeout.com/hdl/testing/).

## Setting up

1. Install Icarus Verilog and `pip install -r requirements.txt`.
2. `PROJECT_SOURCES` already points to `project.v`; [tb.v](tb.v) already instantiates `tt_um_skypiggy8_tinycalc`.
3. Run commands below from this `test` directory. Directed boundary cases and 256 deterministic random operand pairs per operation run in RTL and gate-level modes.

The independent exhaustive generic-gate test covers all 262,144 input combinations:

```sh
cd ..
mkdir -p build
yosys -s scripts/synth.ys > build/synth.log
python scripts/gate_test.py
```

It also checks enable-pause and reset during an operation. This is not extracted-layout simulation.

## How to run

To run the RTL simulation:

```sh
make -B
```

To run gatelevel simulation, first harden your project and copy `../runs/wokwi/results/final/verilog/gl/{your_module_name}.v` to `gate_level_netlist.v`.

Then run:

```sh
make -B GATES=yes
```

If you wish to save the waveform in VCD format instead of FST format, edit tb.v to use `$dumpfile("tb.vcd");` and then run:

```sh
make -B FST=
```

This will generate `tb.vcd` instead of `tb.fst`.

## How to view the waveform file

Using GTKWave

```sh
gtkwave tb.fst tb.gtkw
```

Using Surfer

```sh
surfer tb.fst
```
