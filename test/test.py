# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def dual_function(dut):
    dut.clk.value=0;dut.rst_n.value=0;dut.ena.value=1
    dut.ui_in.value=0;dut.uio_in.value=0
    async def tick():
        dut.clk.value=0
        await Timer(10,unit="ns")
        dut.clk.value=1
        await Timer(10,unit="ns")
    await tick();dut.rst_n.value=1
    assert int(dut.uio_oe.value)==0xc0
    assert (int(dut.uo_out.value)&0x88)==0x88
    # Calculate 123 + 45 and read back 16 serial bits without stopping VGA.
    dut.ui_in.value=123;dut.uio_in.value=1;await tick()
    dut.ui_in.value=45;dut.uio_in.value=2;await tick()
    dut.uio_in.value=4;await tick()
    dut.uio_in.value=0
    assert (int(dut.uio_out.value)&0x40)==0
    bits=[]
    for b in range(16):
        dut.ui_in.value=(b//8)*16+(b%8)
        await Timer(1,unit="ns")
        bits.append((int(dut.uio_out.value)>>7)&1)
    assert sum(bit<<i for i,bit in enumerate(bits))==168
    assert (int(dut.uo_out.value)&0x88)==0x88
    for _ in range(800):
        await tick()
    assert int(dut.user_project.x.value)==3  # three operand / START cycles already elapsed
