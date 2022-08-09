import re


class Rule:
    def __init__(self, must_be_finished, before_beginning):
        self.must_be_finished = must_be_finished
        self.before_beginning = before_beginning
    def __repr__(self):
        return f'{self.must_be_finished} must be finished before beginning {self.before_beginning}'

def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
        return data

def build_graph(data):
    for line in data:
        result = re.search('^Step (\w) must be finished before step (\w) can begin.$', line)
        must_be_finished = result.group(1)
        before_beginning = result.group(2)
        rule = Rule(must_be_finished, before_beginning)
        print(rule)

def part_one():
    filename = 'Day_07_small_data.txt'
    data = read_puzzle_data(filename)
    build_graph(data)

part_one()