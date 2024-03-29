import unittest
"""
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
"""

def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data: str):
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
        self.assertEqual(-1, part_one('Day_08_data.txt'))
        self.assertEqual(-1, part_one('Day_08_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_08_data.txt'))
        self.assertEqual(-1, part_two('Day_08_short_data.txt'))
