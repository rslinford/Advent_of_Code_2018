import re
import unittest
import numpy as np


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class Claim:
    def __init__(self, claim_text):
        result = re.search(r'^#([^ ]+) @ (\d+),(\d+): (\d+)x(\d+)', claim_text)
        self.id = result.group(1)
        self.x, self.y = int(result.group(2)), int(result.group(3))
        self.width = int(result.group(4))
        self.height = int(result.group(5))

    def __repr__(self):
        return f'Claim id:{self.id} x:{self.x} y:{self.y} width:{self.width} height:{self.height}'

    def __eq__(self, other):
        return self.id == other.id


def mark_claims(claim_data, grid_size):
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for claim_text in claim_data:
        claim = Claim(claim_text)
        for y in range(claim.y, claim.y + claim.height):
            for x in range(claim.x, claim.x + claim.width):
                grid[y][x] += 1
    return grid

def mark_claims_except_one(claim_data, grid_size, except_this_claim):
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for claim_text in claim_data:
        claim = Claim(claim_text)
        if claim == except_this_claim:
            continue
        for y in range(claim.y, claim.y + claim.height):
            for x in range(claim.x, claim.x + claim.width):
                grid[y][x] += 1
    return grid

def check_for_space(grid, claim):
    for y in range(claim.y, claim.y + claim.height):
        for x in range(claim.x, claim.x + claim.width):
            if grid[y][x] != 0:
                return False
    return True


def tally_two_or_greater(grid):
    tally = 0
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y][x] > 1:
                tally += 1
    return tally


def part_01(filename, grid_size):
    data = read_puzzle_data(filename)
    grid = mark_claims(data, grid_size)
    return tally_two_or_greater(grid)

def part_02(filename, grid_size):
    claim_data = read_puzzle_data(filename)
    for claim_text in claim_data:
        claim = Claim(claim_text)
        grid = mark_claims_except_one(claim_data, grid_size, claim)
        if check_for_space(grid, claim):
            print(f'There is room for this one: {claim}')
            return claim.id



# print(f'Squares: {part_01("Day_03_data.txt", 1001)}')

print(f'Squares: {part_02("Day_03_data.txt", 1001)}')

class Test(unittest.TestCase):
    def test_part_01(self):
        result = part_01('Day_03_short_data.txt', 11)
        self.assertEqual(4, result)
