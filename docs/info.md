# TinyCalc

## How it works

Unsigned 8-bit operands A and B; 16-bit result. OP 0 adds, OP 1 subtracts,
OP 2 multiplies, OP 3 divides with integer truncation. Negative subtraction
results are 16-bit two's complement; other operations have unsigned results.
255*255 = 65025. Division by zero returns 0xffff and raises DIVZERO.

One shared 16-bit add/subtract datapath performs multiplication by repeated
addition and division by repeated subtraction. This deliberately trades latency
for a simple datapath. It is an area-oriented baseline, not a proven minimum.

## How to test

All inputs are synchronous to clk; hold data stable around its rising edge.
Assert each strobe for exactly one rising edge, then deassert it.

1. Reset rst_n low for at least one rising edge, then high. Keep ena high.
2. Set ui_in=A; pulse uio[0] (LOAD_A).
3. Set ui_in=B; pulse uio[1] (LOAD_B).
4. Set uio[4:3]=OP; pulse uio[2] (START).
5. Deassert strobes. Wait until uio[6] (BUSY) is low.
6. Set uio[5]=0 and read uo_out for low byte; set it to 1 for high byte.
7. Read uio[7] for DIVZERO.

Always reload A/B for each calculation. Read results only when BUSY=0.
Add/subtract and division-by-zero finish on START. Multiplication takes A
additional clock cycles (zero takes none); division takes floor(A/B)+1.
Maximum ordinary busy period: 256 clocks. A high-priority reset aborts operation.
ena=0 pauses state updates. While busy, operand loads/start are ignored.
When idle, priority is LOAD_A > LOAD_B > START. uio[7:6] are chip outputs;
the host must not drive them. uio[5:0] are chip inputs.

## External hardware

External controller or synchronous switches, optional keypad/display and proper
level conversion. The chip computes arithmetic; the host handles UI only.
The current physical layout is unfinished; see physical_status.md.
