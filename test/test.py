# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def vga_basic(dut):
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    async def tick():
        dut.clk.value = 0
        await Timer(10, unit="ns")
        dut.clk.value = 1
        await Timer(10, unit="ns")
    await tick()
    dut.rst_n.value = 1
    assert int(dut.uio_oe.value) == 0
    assert int(dut.uo_out.value) & 0x88 == 0x88
    for _ in range(800):
        await tick()
    # After 800 clocks, horizontal position resets and vertical advances
    assert int(dut.user_project.x.value) == 0
    assert int(dut.user_project.y.value) == 1
    assert int(dut.uo_out.value) & 0x88 == 0x88
