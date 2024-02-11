import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data):
    return data.splitlines()


class Grid(dict):
    def __init__(self, lines):
        super().__init__()
        self.height = len(lines)
        self.width = len(lines[0])
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                self[(x, y)] = c

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self[(x,y)], end='')
            print()


def part_one(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    g = Grid(data)
    g.print()

    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_15_data.txt'))
        self.assertEqual(-1, part_one('Day_15_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_15_data.txt'))
        self.assertEqual(-1, part_two('Day_15_short_data.txt'))
