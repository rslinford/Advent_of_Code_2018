import re


def find_max_x_and_max_y(points):
    max_x, max_y = 0, 0
    for point in points:
        if max_x < point[0]:
            max_x = point[0]
        if max_y < point[1]:
            max_y = point[1]
    return max_x, max_y


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
    max_x, max_y = find_max_x_and_max_y(points)
    square = max(max_x, max_y)
    print(square)


part_one()
