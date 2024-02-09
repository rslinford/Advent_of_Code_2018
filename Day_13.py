import unittest
from dataclasses import dataclass
from enum import Enum, auto


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


class Heading(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

@dataclass
class Cart:
    x: int
    y: int
    heading: Heading


def scan_for_carts(grid):
    carts = []
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            match grid[y][x]:
                case '^':
                    heading = Heading.UP
                case 'v':
                    heading = Heading.DOWN
                case '<':
                    heading = Heading.LEFT
                case '>':
                    heading = Heading.RIGHT
                case _:
                    heading = None
            if heading:
                carts.append(Cart(x, y, heading))
    return carts


def parse_data(data):
    grid = [list(a) for a in data.split('\n')]
    longest = 0
    for row in grid:
        longest = max(longest, len(row))
    for row in grid:
        while len(row) < longest:
            row.append(' ')
    carts = scan_for_carts(grid)
    return grid, carts


def part_one(filename):
    data = read_puzzle_input(filename)
    grid, carts = parse_data(data)
    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_13_data.txt'))
        self.assertEqual(-1, part_one('Day_13_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_13_data.txt'))
        self.assertEqual(-1, part_two('Day_13_short_data.txt'))
