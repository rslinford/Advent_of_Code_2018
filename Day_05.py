import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return list(data)


def part_one(filename):
    polymer = read_puzzle_data(filename)
    has_changed = True
    while has_changed:
        print('Polymer: ' + ''.join(polymer))
        has_changed = False
        next_polymer = []
        i = 0
        while i < len(polymer) - 1:
            if abs(ord(polymer[i]) - ord(polymer[i+1])) != 32:
                next_polymer.append(polymer[i])
                i += 1
                continue
            has_changed = True
            i += 2
        next_polymer.append(polymer[-1])
        polymer = next_polymer
    return ''.join(polymer)


part_one('Day_05_short_data.txt')


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual('dabCBAcaDA', part_one('Day_05_short_data.txt'))