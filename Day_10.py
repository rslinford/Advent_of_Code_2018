import re
import unittest
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class LightPoint:
    position: tuple[int, int]
    velocity: tuple[int, int]


def parse_data(data: str):
    points = []
    for row in data.splitlines():
        result = re.findall(r'-?\d+', row)
        points.append(LightPoint((int(result[0]), int(result[1])), (int(result[2]), int(result[3]))))
    return data


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
        # self.assertEqual(-1, part_one('Day_10_data.txt'))
        self.assertEqual(-1, part_one('Day_10_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_10_data.txt'))
        self.assertEqual(-1, part_two('Day_10_short_data.txt'))
