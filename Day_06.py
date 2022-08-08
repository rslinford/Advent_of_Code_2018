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


def create_grid(grid_size):
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


def survey_the_boarder(grid):
    letters = set()
    for x in range(len(grid)):
        letter = grid[0][x]
        if ord(letter) >= ord('a'):
            letters.add(letter)
    for x in range(len(grid)):
        letter = grid[len(grid) - 1][x]
        if ord(letter) >= ord('a'):
            letters.add(letter)
    for y in range(len(grid)):
        letter = grid[y][0]
        if ord(letter) >= ord('a'):
            letters.add(letter)
    for y in range(len(grid)):
        letter = grid[y][len(grid) - 1]
        if ord(letter) >= ord('a'):
            letters.add(letter)
    print(f'Letters on the boarder: {letters}')
    return letters

def count_letter(letter, grid):
    tally = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            letter_upper = chr(ord(letter) - 32)
            if grid[y][x] == letter or grid[y][x] == letter_upper :
                tally += 1

    return tally


def rank_largest_landlocked(points, grid, letters):
    largest = 0
    for i,point in enumerate(points):
        letter = chr(ord('a') + i)
        if letter not in letters:
            n = count_letter(letter, grid)
            if n > largest:
                largest = n
    return largest



def part_one():
    points = read_puzzle_data('Day_06_short_data.txt')
    grid_size = size_the_grid(points)
    grid = create_grid(grid_size)
    draw_points_on_grid(points, grid)
    map_closest_coordinates(points, grid)
    letters = survey_the_boarder(grid)
    size = rank_largest_landlocked(points, grid, letters)
    print(render_grid(grid))
    print(f'Size of largest landlocked: {size}')




part_one()

#
# class Test(unittest.TestCase):
#     def test_measure_distances(self):
#         pass
#
#     def test_pick_closest_point(self):
#         pass
