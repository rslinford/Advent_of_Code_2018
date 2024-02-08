import re
import unittest
from collections import defaultdict


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data


def parse_data(data: str):
    points = set()
    for row in data.splitlines():
        points.add(tuple(map(int, re.findall(r'\d+', row))))
    return points


def neighbors_of(location):
    x, y = location
    return [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y),
            (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)]


def calculate_manhattan_distance(location1, location2):
    x1, y1 = location1
    x2, y2 = location2
    return abs(x1 - x2) + abs(y1 - y2)


def find_closest_point(points, location):
    smallest_distance = float('inf')
    closest_point = None
    for point in points:
        distance = calculate_manhattan_distance(point, location)
        if distance < smallest_distance:
            smallest_distance = distance
            closest_point = point
        elif distance == smallest_distance:
            closest_point = None
    return closest_point


def in_bounds(min_xy, max_xy, location):
    return all(min_xy[i] <= location[i] <= max_xy[i] for i in range(2))


def scan(points, min_xy, max_xy):
    min_x, min_y = min_xy
    max_x, max_y = max_xy
    counts = defaultdict(int)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            closest_point = find_closest_point(points, (x, y))
            if closest_point:
                counts[closest_point] += 1
    return counts


def weed_out_infinities(points, min_xy, max_xy, counts: dict[tuple, int]):
    min_x, min_y = min_xy
    max_x, max_y = max_xy
    for x in range(min_x, max_x + 1):
        closest_point = find_closest_point(points, (x, min_y))
        if closest_point and counts[closest_point]:
            del counts[closest_point]
        closest_point = find_closest_point(points, (x, max_y))
        if closest_point and counts[closest_point]:
            del counts[closest_point]
    for y in range(min_y, max_y + 1):
        closest_point = find_closest_point(points, (min_x, y))
        if closest_point and counts[closest_point]:
            del counts[closest_point]
        closest_point = find_closest_point(points, (max_x, y))
        if closest_point and counts[closest_point]:
            del counts[closest_point]


def calculate_boundaries(points):
    border = 10
    min_xy = tuple(min(p[i] - border for p in points) for i in range(2))
    max_xy = tuple(max(p[i] + border for p in points) for i in range(2))
    return min_xy, max_xy


def part_one(filename):
    data = read_puzzle_input(filename)
    points = parse_data(data)
    min_xy, max_xy = calculate_boundaries(points)
    counts = scan(points, min_xy, max_xy)
    weed_out_infinities(points, min_xy, max_xy, counts)
    s = sorted(counts.values(), reverse=True)
    return s[0]


def find_region(points, min_xy, max_xy, max_distance):
    region_size = 0
    min_x, min_y = min_xy
    max_x, max_y = max_xy
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            distance = 0
            for point in points:
                distance += calculate_manhattan_distance((x, y), point)
            if distance < max_distance:
                region_size += 1

    return region_size


def part_two(filename, max_distance):
    data = read_puzzle_input(filename)
    points = parse_data(data)
    min_xy, max_xy = calculate_boundaries(points)
    region_size = find_region(points, min_xy, max_xy, max_distance)
    return region_size


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(-1, part_one('Day_06_data.txt'))
        self.assertEqual(17, part_one('Day_06_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(35334, part_two('Day_06_data.txt', 10000))
        self.assertEqual(16, part_two('Day_06_short_data.txt', 32))

    def test_find_closest_point(self):
        data = read_puzzle_input('Day_06_short_data.txt')
        points = parse_data(data)
        self.assertEqual((1, 1), find_closest_point(points, (0, 0)))
        self.assertIsNone(find_closest_point(points, (0, 4)))
        self.assertEqual((1, 6), find_closest_point(points, (0, 5)))
        self.assertEqual((1, 6), find_closest_point(points, (1, 6)))

    # noinspection PyTypeChecker
    def test_scan(self):
        data = read_puzzle_input('Day_06_short_data.txt')
        points = parse_data(data)
        min_xy, max_xy = calculate_boundaries(points)
        counts = scan(points, min_xy, max_xy)
        self.assertEqual(9, counts[(3, 4)])
        self.assertEqual(17, counts[(5, 5)])
        self.assertEqual(0, counts[None])

    # noinspection PyTypeChecker
    def test_weed_out_infinities(self):
        data = read_puzzle_input('Day_06_short_data.txt')
        points = parse_data(data)
        min_xy, max_xy = calculate_boundaries(points)
        counts = scan(points, min_xy, max_xy)
        weed_out_infinities(points, min_xy, max_xy, counts)
        self.assertEqual(0, counts[(1, 1)])
        self.assertEqual(17, counts[(5, 5)])
