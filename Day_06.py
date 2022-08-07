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




def part_one():
    points = read_puzzle_data('Day_06_short_data.txt')
    print(points)


part_one()


class Test(unittest.TestCase):
    def test_measure_distances(self):
        pass

    def test_pick_closest_point(self):
        pass
