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


HEADING_TO_CHAR = {Heading.UP: '^', Heading.DOWN: 'v', Heading.LEFT: '<', Heading.RIGHT: '>'}

HEADING_TO_DXDY = {Heading.UP: (0, -1), Heading.DOWN: (0, 1), Heading.LEFT: (-1, 0), Heading.RIGHT: (1, 0)}


class Go(Enum):
    LEFT = auto()
    STRAIGHT = auto()
    RIGHT = auto()


@dataclass
class Cart:
    x: int
    y: int
    heading: Heading
    next_turn = Go.LEFT
    tick_id = None

    def move(self, tick_id):
        dx, dy = HEADING_TO_DXDY[self.heading]
        self.x += dx
        self.y += dy
        self.tick_id = tick_id

    def encounter(self, c):
        if c == '|' or c == '-':
            return
        if c == '/':
            match self.heading:
                case Heading.UP:
                    self.heading = Heading.RIGHT
                case Heading.DOWN:
                    self.heading = Heading.LEFT
                case Heading.LEFT:
                    self.heading = Heading.DOWN
                case Heading.RIGHT:
                    self.heading = Heading.UP
        elif c == '\\':
            match self.heading:
                case Heading.UP:
                    self.heading = Heading.LEFT
                case Heading.DOWN:
                    self.heading = Heading.RIGHT
                case Heading.LEFT:
                    self.heading = Heading.UP
                case Heading.RIGHT:
                    self.heading = Heading.DOWN
        elif c == '+':
            match self.next_turn:
                case Go.LEFT:
                    match self.heading:
                        case Heading.UP:
                            self.heading = Heading.LEFT
                        case Heading.DOWN:
                            self.heading = Heading.RIGHT
                        case Heading.LEFT:
                            self.heading = Heading.DOWN
                        case Heading.RIGHT:
                            self.heading = Heading.UP
                    self.next_turn = Go.STRAIGHT
                case Go.STRAIGHT:
                    self.next_turn = Go.RIGHT
                case Go.RIGHT:
                    match self.heading:
                        case Heading.UP:
                            self.heading = Heading.RIGHT
                        case Heading.DOWN:
                            self.heading = Heading.LEFT
                        case Heading.LEFT:
                            self.heading = Heading.UP
                        case Heading.RIGHT:
                            self.heading = Heading.DOWN
                    self.next_turn = Go.LEFT

        else:
            assert False, f'Cart off the rails. Encountered "{c}"'


def scan_for_carts(grid):
    carts = []
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            match grid[y][x]:
                case '^':
                    heading = Heading.UP
                    grid[y][x] = '|'
                case 'v':
                    heading = Heading.DOWN
                    grid[y][x] = '|'
                case '<':
                    heading = Heading.LEFT
                    grid[y][x] = '-'
                case '>':
                    heading = Heading.RIGHT
                    grid[y][x] = '-'
                case _:
                    heading = None
            if heading:
                carts.append(Cart(x, y, heading))
    return carts


def look_up_cart(carts, x, y):
    for cart in carts:
        if cart.x == x and cart.y == y:
            return cart
    return None


def print_grid(grid, carts):
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            cart = look_up_cart(carts, x, y)
            if cart:
                print(HEADING_TO_CHAR[cart.heading], end='')
            else:
                print(grid[y][x], end='')
        print()


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


def detect_collision(carts, most_recently_moved_cart):
    count = 0
    for cart in carts:
        if cart.x == most_recently_moved_cart.x and cart.y == most_recently_moved_cart.y:
            count += 1
    return count > 1


def one_tick(grid, carts, tick_id):
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            cart = look_up_cart(carts, x, y)
            if not cart or cart.tick_id == tick_id:
                continue
            cart.move(tick_id)
            if detect_collision(carts, cart):
                return cart.x, cart.y
            cart.encounter(grid[cart.y][cart.x])
    return None


def find_cart_at(carts, x, y):
    for cart in carts:
        if cart.x == x and cart.y == y:
            return cart
    return None


def remove_carts_at(carts, x, y):
    while cart := find_cart_at(carts, x, y):
        carts.remove(cart)


def one_tick_part_two(grid, carts, tick_id):
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            cart = look_up_cart(carts, x, y)
            if not cart or cart.tick_id == tick_id:
                continue
            cart.move(tick_id)
            if detect_collision(carts, cart):
                remove_carts_at(carts, cart.x, cart.y)
            cart.encounter(grid[cart.y][cart.x])


def part_one(filename):
    data = read_puzzle_input(filename)
    grid, carts = parse_data(data)
    collision = None
    tick_id = 0
    while not collision:
        # print()
        # print_grid(grid, carts)
        collision = one_tick(grid, carts, tick_id)
        tick_id += 1
    return collision


def part_two(filename):
    data = read_puzzle_input(filename)
    grid, carts = parse_data(data)
    tick_id = 0
    while not len(carts) == 1:
        # print()
        # print_grid(grid, carts)
        one_tick_part_two(grid, carts, tick_id)
        tick_id += 1
    return carts[0].x, carts[0].y


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual((38, 72), part_one('Day_13_data.txt'))
        self.assertEqual((7, 3), part_one('Day_13_short_data.txt'))

    def test_part_two(self):
        self.assertEqual((68, 27), part_two('Day_13_data.txt'))
        self.assertEqual((6, 4), part_two('Day_13_short_data2.txt'))
