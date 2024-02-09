import unittest

GRID_SIZE = 300
SQUARE_SIZE = 3


def calculate_fuel_cell_power(serial_number, x, y):
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    if power < 100:
        return 0
    power = str(power)
    hundreds = power[-3]
    return int(hundreds) - 5


def calculate_square_power(serial_number, x_corner, y_corner):
    total_power = 0
    for y in range(y_corner, y_corner + SQUARE_SIZE):
        for x in range(x_corner, x_corner + SQUARE_SIZE):
            total_power += calculate_fuel_cell_power(serial_number, x, y)
    return total_power


def part_one(serial_number):
    max_power = -float('inf')
    max_xy = None
    for y in range(1, GRID_SIZE - SQUARE_SIZE + 2):
        for x in range(1, GRID_SIZE - SQUARE_SIZE + 2):
            power = calculate_square_power(serial_number, x, y)
            if power > max_power:
                max_power = power
                max_xy = (x, y)
    return max_xy


def part_two():
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual((21, 93), part_one(1955))
        self.assertEqual((33, 45), part_one(18))

    def test_part_two(self):
        self.assertEqual(-1, part_two())
        self.assertEqual(-1, part_two())

    def test_calculate_fuel_cell_power(self):
        self.assertEqual(4, calculate_fuel_cell_power(8, 3, 5))
        self.assertEqual(-5, calculate_fuel_cell_power(57, 122, 79))
        self.assertEqual(0, calculate_fuel_cell_power(39, 217, 196))
        self.assertEqual(4, calculate_fuel_cell_power(71, 101, 153))