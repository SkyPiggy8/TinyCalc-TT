# SPDX-License-Identifier: Apache-2.0
import random
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def calculator(dut):
    async def tick():
        dut.clk.value=0
        await Timer(5,unit='us')
        dut.clk.value=1
        await Timer(5,unit='us')
    dut.clk.value=0;dut.ena.value=1;dut.ui_in.value=0;dut.uio_in.value=0;dut.rst_n.value=0
    await tick();dut.rst_n.value=1
    rng=random.Random(20261102)
    values=[0,1,2,3,127,128,254,255]
    for op in range(4):
        pairs=[(a,b) for a in values for b in values]+[(rng.randrange(256),rng.randrange(256)) for _ in range(256)]
        for a,b in pairs:
            dut.ui_in.value=a;dut.uio_in.value=1;await tick()
            dut.ui_in.value=b;dut.uio_in.value=2;await tick()
            dut.uio_in.value=4|(op<<3);await tick();dut.uio_in.value=op<<3
            for _ in range(258):
                if not(int(dut.uio_out.value)&64):break
                await tick()
            else:assert False,'BUSY timeout'
            dut.uio_in.value=0;await Timer(1,unit='us');lo=int(dut.uo_out.value)
            dut.uio_in.value=32;await Timer(1,unit='us');got=lo|(int(dut.uo_out.value)<<8)
            expected=[a+b,(a-b)&65535,a*b,a//b if b else 65535][op]
            assert got==expected,(op,a,b,got,expected)
            assert bool(int(dut.uio_out.value)&128)==(op==3 and b==0)
            assert int(dut.uio_oe.value)==192
