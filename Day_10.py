import re
import unittest
from dataclasses import dataclass
from typing import List


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class LightPoint:
    position: tuple[int, int]
    velocity: tuple[int, int]


def parse_data(data: str) -> List[LightPoint]:
    points = []
    for row in data.splitlines():
        result = re.findall(r'-?\d+', row)
        points.append(LightPoint((int(result[0]), int(result[1])), (int(result[2]), int(result[3]))))
    return points


def find_boundaries(points: List[LightPoint]):
    min_xy = tuple(min(p.position[i] for p in points) for i in range(2))
    max_xy = tuple(max(p.position[i] for p in points) for i in range(2))
    return min_xy, max_xy


def light_on(points: List[LightPoint], location):
    x1, y1 = location
    for p in points:
        x2, y2 = p.position
        if x1 == x2 and y1 == y2:
            return True
    return False


def print_points(points):
    min_xy, max_xy = find_boundaries(points)
    min_x, min_y = min_xy
    max_x, max_y = max_xy
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if light_on(points, (x, y)):
                print('#', end='')
            else:
                print('.', end='')
        print()

def calculate_field_size(points):
    min_xy, max_xy = find_boundaries(points)
    min_x, min_y = min_xy
    max_x, max_y = max_xy
    return (max_x - min_x) * (max_y - min_y)



def advance_one_second(points):
    for point in points:
        px, py = point.position
        vx, vy = point.velocity
        px += vx
        py += vy
        point.position = (px, py)


def reverse_one_second(points):
    for point in points:
        px, py = point.position
        vx, vy = point.velocity
        px -= vx
        py -= vy
        point.position = (px, py)


def part_one(filename):
    data = read_puzzle_input(filename)
    points = parse_data(data)
    field_getting_smaller = True
    field_size = calculate_field_size(points)
    elapsed_seconds = 0
    while field_getting_smaller:
        advance_one_second(points)
        elapsed_seconds += 1
        new_field_size = calculate_field_size(points)
        if new_field_size > field_size:
            field_getting_smaller = False
        field_size = new_field_size
    reverse_one_second(points)
    elapsed_seconds -= 1
    print_points(points)
    return elapsed_seconds


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(10375, part_one('Day_10_data.txt'))
        self.assertEqual(3, part_one('Day_10_short_data.txt'))
