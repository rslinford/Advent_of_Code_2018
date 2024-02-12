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
        before = re.findall(r'\d+', bad[0])
        instruction = re.findall(r'\d+', bad[1])
        after = re.findall(r'\d+', bad[2])
        samples.append(Sample(before, instruction, after))
    return samples


def part_one(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_16_data.txt'))
        self.assertEqual(-1, part_one('Day_16_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_16_data.txt'))
        self.assertEqual(-1, part_two('Day_16_short_data.txt'))
