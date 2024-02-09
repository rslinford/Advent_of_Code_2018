import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data




def parse_data(data):
    data = data.split('\n')
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
        self.assertEqual(-1, part_one('Day_13_data.txt'))
        self.assertEqual(-1, part_one('Day_13_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_13_data.txt'))
        self.assertEqual(-1, part_two('Day_13_short_data.txt'))
