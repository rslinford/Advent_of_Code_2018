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
    return max(max_x, max_y) + 1


def create_grid(points, grid_size):
    rval = []
    for _ in range(grid_size + 1):
        rval.append(['.'] * (grid_size + 1))
    return rval

def render_grid(grid):
    rval = []
    for y in range(len(grid)):
        rval.append(''.join(grid[y]))
        rval.append('\n')
    return ''.join(rval)


def draw_points_on_grid(points, grid):
    for i, point in enumerate(points):
        point_label = chr(ord('A') + i)
        grid[point[1]][point[0]] = point_label


def not_a_tie(x, y, points, shortest_distance):
    tally = 0
    for i, point in enumerate(points):
        distance = abs(y - point[1]) + abs(x - point[0])
        if distance == shortest_distance:
            tally += 1
            if tally > 1:
                return False
    return True



def map_closest_coordinates(points, grid):
    for y in range(len(grid)):
        for x in range(len(grid)):
            if (x, y) in points:
                continue
            shortest_distance = math.inf
            closest_point_index = None
            for i, point in enumerate(points):
                distance = abs(y - point[1]) + abs(x - point[0])
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_point_index = i
            if not_a_tie(x, y, points, shortest_distance):
                if closest_point_index != None:
                    grid[y][x] = chr(ord('a') + closest_point_index)



def part_one():
    points = read_puzzle_data('Day_06_short_data.txt')
    grid_size = size_the_grid(points)
    grid = create_grid(points, grid_size)
    draw_points_on_grid(points, grid)
    map_closest_coordinates(points, grid)
    print(render_grid(grid))




part_one()

#
# class Test(unittest.TestCase):
#     def test_measure_distances(self):
#         pass
#
#     def test_pick_closest_point(self):
#         pass
