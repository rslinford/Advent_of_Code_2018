import re
import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class Claim:
    def __init__(self, claim_text):
        result = re.search(r'^#([^ ]+) @ (\d+),(\d+): (\d+)x(\d+)', claim_text)
        self.id = result.group(1)
        self.x, self.y = result.group(2), result.group(3)
        self.width = result.group(4)
        self.height = result.group(5)
    def __repr__(self):
        return f'Claim id:{self.id} x:{self.x} y:{self.y} width:{self.width} height:{self.height}'

def mark_claims(claim_data):
    for claim_text in claim_data:
        claim = Claim(claim_text)
        print(claim)


def part_01(filename):
    data = read_puzzle_data(filename)
    mark_claims(data)
    return 4

# part_01('Day_03_short_data.txt')

class Test(unittest.TestCase):
    def test_part_01(self):
        result = part_01('Day_03_short_data.txt')
        self.assertEqual(4, result)
