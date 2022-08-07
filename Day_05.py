import math
import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return list(data)


def fully_react(polymer):
    has_changed = True
    while has_changed:
        # print('Polymer: ' + ''.join(polymer))
        has_changed = False
        next_polymer = []
        i = 0
        while i < len(polymer) - 1:
            if abs(ord(polymer[i]) - ord(polymer[i + 1])) != 32:
                next_polymer.append(polymer[i])
                i += 1
                continue
            has_changed = True
            i += 2
        next_polymer.append(polymer[-1])
        polymer = next_polymer
    return polymer


def part_one(filename):
    polymer = read_puzzle_data(filename)
    polymer = fully_react(polymer)
    return ''.join(polymer)


def remove_unit_type(polymer: list, upper_case_char: chr):
    polymer = list(''.join(polymer).replace(upper_case_char, ''))
    lower_case_char = chr(ord(upper_case_char) + 32)
    polymer = list(''.join(polymer).replace(lower_case_char, ''))
    return polymer


def part_two(filename):
    polymer = read_puzzle_data(filename)
    shortest_length = math.inf
    unit_type = None
    for n in range(ord('A'), ord('Z') + 1):
        previous_polymer = polymer
        polymer = remove_unit_type(polymer, chr(n))
        polymer = fully_react(polymer)
        if len(polymer) < shortest_length:
            shortest_length = len(polymer)
            unit_type = chr(n)
            print(f'unit type {unit_type} length {shortest_length} {"".join(polymer)}')
        polymer = previous_polymer
    return unit_type, shortest_length


unit_type, shortest_length = part_two('Day_05_data.txt')
print(f'unit_type {unit_type}   shortest length {shortest_length}')
# print(f'\nResulting polymer length: {len(result)}\n{"".join(result)}')


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual('dabCBAcaDA', part_one('Day_05_short_data.txt'))
    def test_remove_unit_type(self):
        self.assertEqual(['A', 'a', 'B', 'b'], remove_unit_type(list('AxaxBxb'), 'X'))
        self.assertEqual(['A', 'a', 'B', 'b'], remove_unit_type(list('AaBb'), 'X'))
        self.assertEqual(['b', 'e', 'f', 'G'], remove_unit_type(list('abaeafaG'), 'A'))
    def test_part_two(self):
        unit_type, shortest_length = part_two('Day_05_short_data.txt')
        self.assertEqual('C', unit_type)
        self.assertEqual(4, shortest_length)
if __name__ == '__main__':
    unittest.main()