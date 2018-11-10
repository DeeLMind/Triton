#!/usr/bin/env python2
# coding: utf-8
"""Test disassembly."""

import unittest
from triton import *

class TestAArch64Disass(unittest.TestCase):

    """Testing the AArch64 Architecture diassembly."""

    def setUp(self):
        """Define the arch."""
        self.ctx = TritonContext()
        self.ctx.setArchitecture(ARCH.AARCH64)

    def test_inst1(self):
        inst = Instruction("\x80\x46\xc2\xd2") # movz x0, #0x1234, lsl #32

        self.ctx.disassembly(inst)
        self.assertEqual(inst.getDisassembly(), "movz x0, #0x1234, lsl #32")

        self.assertEqual(len(inst.getOperands()), 2)

        op0 = inst.getOperands()[0]
        op1 = inst.getOperands()[1]

        self.assertEqual(op0.getName(), "x0")
        self.assertEqual(op1.getValue(), 0x1234)
        self.assertEqual(op1.getShiftType(), SHIFT.AARCH64.LSL)
        self.assertEqual(op1.getShiftValue(), 32)

    def test_inst2(self):
        inst = Instruction("\xe1\x0b\x40\xb9") # ldr w1, [sp, #8]

        self.ctx.disassembly(inst)
        self.assertEqual(inst.getDisassembly(), "ldr w1, [sp, #8]")

        self.assertEqual(len(inst.getOperands()), 2)

        op0 = inst.getOperands()[0]
        op1 = inst.getOperands()[1]

        self.assertEqual(op0.getName(), "w1")
        self.assertEqual(op0.getSize(), CPUSIZE.DWORD)
        self.assertEqual(op1.getSize(), CPUSIZE.DWORD)
        self.assertEqual(op1.getBaseRegister(), self.ctx.registers.sp)
        self.assertEqual(op1.getDisplacement().getValue(), 8)
        self.assertEqual(op1.getDisplacement().getSize(), CPUSIZE.QWORD)

    def test_inst3(self):
        inst = Instruction("\x20\x08\x02\x8b") # add x0, x1, x2, lsl #2

        self.ctx.disassembly(inst)
        self.assertEqual(inst.getDisassembly(), "add x0, x1, x2, lsl #2")

        self.assertEqual(len(inst.getOperands()), 3)

        op0 = inst.getOperands()[0]
        op1 = inst.getOperands()[1]
        op2 = inst.getOperands()[2]

        self.assertEqual(op0.getName(), "x0")
        self.assertEqual(op0.getSize(), CPUSIZE.QWORD)
        self.assertEqual(op1.getName(), "x1")
        self.assertEqual(op1.getSize(), CPUSIZE.QWORD)
        self.assertEqual(op2.getName(), "x2")
        self.assertEqual(op2.getSize(), CPUSIZE.QWORD)

        self.assertEqual(op0.getShiftType(), SHIFT.AARCH64.INVALID)
        self.assertEqual(op1.getShiftType(), SHIFT.AARCH64.INVALID)
        self.assertEqual(op2.getShiftType(), SHIFT.AARCH64.LSL)
        self.assertEqual(op2.getShiftValue(), 2)
