import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data


def parse_data(data: str):
    return data.split('\n')


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
        self.assertEqual(-1, part_one('Day_06_data.txt'))
        self.assertEqual(-1, part_one('Day_06_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_06_data.txt'))
        self.assertEqual(-1, part_two('Day_06_short_data.txt'))
