import re
import unittest
from collections import defaultdict
from dataclasses import dataclass
from typing import List


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data


@dataclass
class Rule:
    pattern: str
    result: str


class State:
    def __init__(self, string):
        if '#' in string:
            self.left_end = 999999999
            self.right_end = -999999999
        else:
            self.left_end = 0
            self.right_end = 0
        self.d = self._initialize_state(string)

    # noinspection PyTypeChecker
    def __repr__(self):
        string = []
        for i in range(self.left_end, self.right_end + 1):
            string.append(self.d[i])
        return ''.join(string)

    # noinspection PyTypeChecker
    def _initialize_state(self, string):
        d = defaultdict(lambda: '.')
        for i, c in enumerate(string):
            if c == '#':
                d[i] = '#'
                self.left_end = min(self.left_end, i)
                self.right_end = max(self.right_end, i)
        return d

    # noinspection PyTypeChecker
    def string_at(self, pot_id):
        string = []
        for i in range(pot_id - 2, pot_id + 3):
            string.append(self.d[i])
        return ''.join(string)

    def plant(self, i):
        self.left_end = min(self.left_end, i)
        self.right_end = max(self.right_end, i)
        self.d[i] = '#'

    # noinspection PyTypeChecker
    def score(self):
        total = 0
        for i in range(self.left_end, self.right_end + 1):
            if self.d[i] == '#':
                total += i
        return total


def look_up_rule(rules: List[Rule], string):
    for rule in rules:
        if rule.pattern == string:
            return rule
    return None


def parse_data(data: str):
    data = data.split('\n\n')
    result = re.search(r'initial state: (.*)', data[0])
    state = result.group(1)
    data = data[1].split('\n')
    rules = []
    for row in data:
        result = re.search(r'(.....) => (.)', row)
        rules.append(Rule(result.group(1), result.group(2)))

    return State(state), rules


def part_one(filename):
    data = read_puzzle_input(filename)
    state, rules = parse_data(data)
    margin = 3
    print(0, state)
    for g in range(1, 21):
        next_state = State('')
        for i in range(state.left_end - margin, state.right_end + margin + 1):
            s = state.string_at(i)
            rule = look_up_rule(rules, s)
            if rule and rule.result == '#':
                next_state.plant(i)
        state = next_state
        print(g, state)
    return state.score()


def part_two(filename):
    data = read_puzzle_input(filename)
    state, rules = parse_data(data)
    margin = 3
    print(0, state)
    for g in range(1, 50_000_000_001):
        next_state = State('')
        for i in range(state.left_end - margin, state.right_end + margin + 1):
            s = state.string_at(i)
            rule = look_up_rule(rules, s)
            if rule and rule.result == '#':
                next_state.plant(i)
        state = next_state
        print(g, state.score(), state)
    return state.score()


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(3337, part_one('Day_12_data.txt'))
        self.assertEqual(325, part_one('Day_12_short_data.txt'))

    def test_part_two(self):
        self.assertEqual(4300000000349, part_two('Day_12_data.txt'))
        # self.assertEqual(-1, part_two('Day_12_short_data.txt'))
