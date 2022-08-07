import math
import re
import unittest

import numpy as np


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        rval = []
        data = f.read().strip().split('\n')
        for row in data:
            result = re.search(r'^(\d+), (\d+)$', row)
            rval.append((int(result.group(1)), int(result.group(2))))
        return rval


def size_the_grid(points):
    max_x, max_y = -1, -1
    for point in points:
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point[1]
    return max(max_x, max_y)


def create_grid(points, grid_size):
    rval = []
    for _ in range(grid_size):
        rval.append(['.'] * grid_size)
    return rval

def render_grid(grid):
    rval = []
    for y in range(len(grid)):
        rval.append(''.join(grid[y]))
        rval.append('\n')
    return ''.join(rval)


def part_one():
    points = read_puzzle_data('Day_06_short_data.txt')
    grid_size = size_the_grid(points)
    grid = create_grid(points, grid_size)
    print(render_grid(grid))


part_one()


class Test(unittest.TestCase):
    def test_measure_distances(self):
        pass

    def test_pick_closest_point(self):
        pass
