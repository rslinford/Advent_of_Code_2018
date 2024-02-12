import unittest
from collections import deque
from dataclasses import dataclass
from typing import Optional


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


def parse_data(data):
    return data.splitlines()


@dataclass
class Pt:
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            if self.y > other.y:
                return False
            if self.y < other.y:
                return True
            return self.x < other.x
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbors(self):
        return [self + a for a in [Pt(0, -1), Pt(0, 1), Pt(-1, 0), Pt(1, 0)]]


@dataclass
class Unit:
    team: str
    pos: Pt
    attack: int = 3
    hp: int = 200
    alive: bool = True

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.pos == other.pos
        return NotImplemented

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.pos < other.pos
        return NotImplemented

    def move_to(self, pos):
        self.pos = pos


class Grid(dict):
    def __init__(self, lines):
        super().__init__()
        self.height = len(lines)
        self.width = len(lines[0])
        self.units = []
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c in 'GE':
                    self.units.append(Unit(c, Pt(x, y)))
                    self[Pt(x, y)] = '.'
                else:
                    self[Pt(x, y)] = c

    def print(self, overlay={}):
        for y in range(self.height):
            for x in range(self.width):
                pos = Pt(x, y)
                unit = self.unit_at(pos)
                if unit:
                    print(unit.team, end='')
                elif pos in overlay:
                    print(overlay[pos], end='')
                else:
                    print(self[pos], end='')
            print()

    def unit_at(self, pos):
        a = [unit for unit in self.units if pos == unit.pos]
        if not a:
            return None
        assert len(a) == 1, f'Illegal state. Multiple units occupy same space: {a}'
        return a[0]

    def find_all_enemies(self, unit):
        enemies = [a for a in self.units if unit.team != a.team]
        enemies.sort()
        return enemies

    def find_enemies_in_range(self, unit):
        enemies = []
        squares = self.neighbors_of_pos(unit.pos)
        for square in squares:
            other_unit = self.unit_at(square)
            if not other_unit:
                continue
            if other_unit.team != unit.team:
                enemies.append(other_unit)
        enemies.sort()
        return enemies

    def open_neighbors_of_units(self, units):
        positions = []
        for unit in units:
            positions.extend(unit.pos.neighbors())
        positions = self.open_square_filter(positions)
        positions.sort()
        return positions

    def open_neighbors_of_pos(self, pos: Pt):
        positions = pos.neighbors()
        positions = self.open_square_filter(positions)
        positions.sort()
        return positions

    def open_square_filter(self, positions):
        keep = []
        for a in positions:
            if self[a] == '.' and not self.unit_at(a):
                keep.append(a)
        return keep

    def neighbors_of_pos(self, pos: Pt):
        positions = pos.neighbors()
        positions = self.square_filter(positions)
        positions.sort()
        return positions

    def square_filter(self, positions):
        keep = []
        for a in positions:
            if self[a] == '.':
                keep.append(a)
        return keep

    def bfs(self, starting_square):
        frontier = deque()
        frontier.append(starting_square)
        came_from: dict[Pt, Optional[Pt]] = {starting_square: None}
        cost_so_far = {starting_square: 0}

        while frontier:
            current = frontier.popleft()
            for next_pos in self.open_neighbors_of_pos(current):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    frontier.append(next_pos)
                    came_from[next_pos] = current

        return came_from, cost_so_far

    @staticmethod
    def reconstruct_path(came_from, start_pos, goal_pos):
        current = goal_pos
        path = []
        if goal_pos not in came_from:
            return []
        while current != start_pos:
            path.append(current)
            current = came_from[current]
        path.append(start_pos)
        path.reverse()
        return path

    def in_play(self):
        if not self.units or not self.find_all_enemies(self.units[0]):
            return False
        return True


def part_one(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    g = Grid(data)
    while g.in_play():
        g.units.sort()
        for unit in g.units:
            enemies = g.find_enemies_in_range(unit)
            if enemies:
                # todo: attack
                continue  # attack ends unit's turn
            # Move
            candidate_squares = g.open_neighbors_of_pos(unit.pos)
            if not candidate_squares:
                continue  # there are no open squares to move to
            enemies = g.find_all_enemies(unit)
            if not enemies:
                continue  # no enemies on the board
            enemy_squares = g.open_neighbors_of_units(enemies)
            if not enemy_squares:
                continue  # no open squares adjacent to enemies
            came_from, cost_so_far = g.bfs(unit.pos)
            reachable_enemy_squares = []
            for square in enemy_squares:
                if square in cost_so_far:
                    reachable_enemy_squares.append(square)
            if not reachable_enemy_squares:
                continue
            nearest_square = None
            nearest_distance = float('inf')
            for square in reachable_enemy_squares:
                if square in cost_so_far and cost_so_far[square] < nearest_distance:
                    nearest_distance = cost_so_far[square]
                    nearest_square = square
            came_from, cost_so_far = g.bfs(nearest_square)
            closest_candidate = None
            closest_distance = float('inf')
            print()
            g.print(cost_so_far)
            for candidate in candidate_squares:
                if candidate in cost_so_far and cost_so_far[candidate] < closest_distance:
                    closest_distance = cost_so_far[candidate]
                    closest_candidate = candidate
            unit.move_to(closest_candidate)
            print()
            g.print()

    return -1


def part_two(filename):
    data = read_puzzle_input(filename)
    data = parse_data(data)
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one('Day_15_data.txt'))
        self.assertEqual(-1, part_one('Day_15_short_data.txt'))
        # self.assertEqual(-1, part_one('Day_15_short_data3.txt'))

    def test_part_two(self):
        self.assertEqual(-1, part_two('Day_15_data.txt'))
        self.assertEqual(-1, part_two('Day_15_short_data.txt'))

    def test_grid(self):
        data = read_puzzle_input('Day_15_short_data2.txt')
        data = parse_data(data)
        g = Grid(data)
        a = g.unit_at(Pt(1, 1))
        self.assertEqual('G', a.team)
        b = g.unit_at(Pt(2, 1))
        self.assertEqual('E', b.team)
        an = g.open_neighbors_of_units([a])
        self.assertEqual(1, len(an))
        self.assertEqual(Pt(1, 2), an[0])

    def test_pt(self):
        p1 = Pt(2, 3)
        p2 = Pt(2, 1)
        p3 = Pt(2, 3)
        p4 = Pt(1, 5)
        list1 = [p1, p2, p3, p4]
        self.assertTrue(p1 == p3)
        self.assertTrue(p1 != p2)
        self.assertEqual(Pt(4, 4), p1 + p2)
        list1.sort()
        self.assertEqual(p2, list1[0])
        self.assertEqual(p1, list1[1])
        self.assertEqual(p3, list1[2])
        self.assertEqual(p4, list1[3])
        neighbors = p1.neighbors()
        self.assertEqual(Pt(2, 2), neighbors[0])
        self.assertEqual(Pt(2, 4), neighbors[1])
        self.assertEqual(Pt(1, 3), neighbors[2])
        self.assertEqual(Pt(3, 3), neighbors[3])
