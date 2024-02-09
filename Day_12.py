import re
import unittest
from collections import defaultdict
from dataclasses import dataclass


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Rule:
    pattern: str
    result: str


def parse_data(data: str):
    data = data.split('\n\n')
    result = re.search(r'initial state: (.*)', data[0])
    state = result.group(1)
    data = data[1].split('\n')
    rules = []
    for row in data:
        result = re.search(r'(.....) => (.)', row)
        rules.append(Rule(result.group(1), result.group(2)))

    return initialize_state(state), rules

def initialize_state(string):
    d = defaultdict(lambda: '.')
    for i, c in enumerate(string):
        if c == '#':
            # noinspection PyTypeChecker
            d[i] = '#'
    return d

def part_one(filename):
    data = read_puzzle_input(filename)
    state, rules = parse_data(data)

    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_12_data.txt'))
        self.assertEqual(-1, part_one('Day_12_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_12_data.txt'))
        self.assertEqual(-1, part_two('Day_12_short_data.txt'))

