import re
import unittest
from dataclasses import dataclass
from typing import List


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Sample:
    before: List[int]
    instruction: List[int]
    after: List[int]


def parse_data(data):
    data = data.split('\n\n\n')
    sample_data = data[0].split('\n\n')
    samples = []
    for bad in sample_data:
        bad = bad.splitlines()
        before = list(map(int, re.findall(r'\d+', bad[0])))
        instruction = list(map(int, re.findall(r'\d+', bad[1])))
        after = list(map(int, re.findall(r'\d+', bad[2])))
        samples.append(Sample(before, instruction, after))
    instructions = data[1].splitlines()
    return samples, instructions


class Processor:
    def __init__(self):
        self.registers = [0, 0, 0, 0]

    def addr(self, instruction):
        """
        stores into register C the result of adding register A and register B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, instruction):
        """
        stores into register C the result of adding register A and value B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] + b

    def mulr(self, instruction):
        """
        stores into register C the result of multiplying register A and register B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, instruction):
        """
        stores into register C the result of multiplying register A and value B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] * b

    def banr(self, instruction):
        """
        stores into register C the result of the bitwise AND of register A and register B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, instruction):
        """
        stores into register C the result of the bitwise AND of register A and value B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] & b

    def borr(self, instruction):
        """
        stores into register C the result of the bitwise OR of register A and register B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, instruction):
        """
        stores into register C the result of the bitwise OR of register A and value B.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a] | b

    def setr(self, instruction):
        """
        copies the contents of register A into register C.
        """
        op, a, b, c = instruction
        self.registers[c] = self.registers[a]

    def seti(self, instruction):
        """
        stores value A into register C.
        """
        op, a, b, c = instruction
        self.registers[c] = a

    def gtir(self, instruction):
        """
        sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if a > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtri(self, instruction):
        """
        sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if self.registers[a] > b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtrr(self, instruction):
        """
        sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if self.registers[a] > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqir(self, instruction):
        """
        sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if a == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqri(self, instruction):
        """
        sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if self.registers[a] == b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqrr(self, instruction):
        """
        sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        """
        op, a, b, c = instruction
        if self.registers[a] == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0


def build_instruction_set(p):
    return [p.addr, p.addi, p.mulr, p.muli, p.banr, p.bani, p.borr, p.bori, p.setr,
            p.seti, p.gtir, p.gtri, p.gtrr, p.eqir, p.eqri, p.eqrr]


def part_one(filename):
    data = read_puzzle_input(filename)
    samples, instructions = parse_data(data)
    p = Processor()
    method_set = build_instruction_set(p)
    three_or_more_tally = 0
    for sample in samples:
        tally = 0
        for method in method_set:
            p.registers = sample.before.copy()
            method(sample.instruction)
            if p.registers == sample.after:
                tally += 1
        if tally >= 3:
            three_or_more_tally += 1

    return three_or_more_tally


def part_two(filename):
    data = read_puzzle_input(filename)
    samples, instructions = parse_data(data)
    p = Processor()
    method_set = build_instruction_set(p)
    three_or_more_tally = 0
    for sample in samples:
        tally = 0
        for method in method_set:
            p.registers = sample.before.copy()
            method(sample.instruction)
            if p.registers == sample.after:
                tally += 1
        if tally >= 3:
            three_or_more_tally += 1

    return three_or_more_tally


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_16_data.txt'))
        # self.assertEqual(1, part_one('Day_16_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_16_data.txt'))
        self.assertEqual(-1, part_two('Day_16_short_data.txt'))

    def test_processor_addr(self):
        p = Processor()
        p.registers = [4, 7, 8, 5]
        p.addr([0, 1, 2, 3])
        self.assertEqual(4, p.registers[0])
        self.assertEqual(7, p.registers[1])
        self.assertEqual(8, p.registers[2])
        self.assertEqual(15, p.registers[3])

    def test_processor_addi(self):
        p = Processor()
        p.registers = [4, 7, 8, 5]
        p.addi([0, 1, 30, 0])
        self.assertEqual(37, p.registers[0])
        self.assertEqual(7, p.registers[1])
        self.assertEqual(8, p.registers[2])
        self.assertEqual(5, p.registers[3])

    def test_processor_mulr(self):
        p = Processor()
        p.registers = [4, 7, 8, 5]
        p.mulr([0, 0, 2, 1])
        self.assertEqual(32, p.registers[1])

    def test_processor_muli(self):
        p = Processor()
        p.registers = [4, 7, 8, 5]
        p.muli([0, 1, 10, 2])
        self.assertEqual(70, p.registers[2])

    def test_processor_banr(self):
        p = Processor()
        p.registers = [4, 5, 13, 5]
        p.banr([0, 1, 2, 3])
        self.assertEqual(12, p.registers[3])

    def test_processor_bani(self):
        p = Processor()
        p.registers = [4, 12, 5, 21]
        p.bani([0, 3, 255, 0])
        self.assertEqual(21, p.registers[0])

    def test_processor_borr(self):
        p = Processor()
        p.registers = [4, 255, 5, 21]
        p.borr([0, 1, 2, 3])
        self.assertEqual(255, p.registers[3])

    def test_processor_bori(self):
        p = Processor()
        p.registers = [4, 25, 5, 21]
        p.bori([0, 1, 255, 3])
        self.assertEqual(255, p.registers[3])
