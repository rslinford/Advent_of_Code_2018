import re

steps = {}

class Step:
    def __init__(self, name):
        self.name = name
        self.dependencies = []
    def __repr__(self):
        return f'Step({self.name}) dependencies: {self.dependencies}'
    def add_dependency(self, other_step):
        self.dependencies.append(other_step)
    def __lt__(self, other):
        return self.name < other.name

    @staticmethod
    def step_factory(name):
        if name in steps.keys():
            rval = steps.get(name)
        else:
            rval = Step(name)
            steps[name] = rval
        return rval



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
        a = Step.step_factory(must_be_finished)
        b = Step.step_factory(before_beginning)
        b.add_dependency(a)
        print(b)


def find_step_with_zero_dependencies():
    zeros = []
    for step in steps.values():
        if len(step.dependencies) == 0:
            zeros.append(step)
    if len(zeros) == 0:
        assert('Bad data leaves us stuck here')
    zeros.sort()
    return zeros[0]


def remove_step_as_a_dependency(step: Step):
    for other_step in steps.values():
        if step in other_step.dependencies:
            other_step.dependencies.remove(step)


def part_one():
    filename = 'Day_07_data.txt'
    data = read_puzzle_data(filename)
    build_graph(data)
    step_order = []
    while len(steps.keys()) > 0:
        step = find_step_with_zero_dependencies()
        remove_step_as_a_dependency(step)
        steps.pop(step.name)
        step_order.append(step.name)
    order = ''.join(step_order)
    print(f'Completed order {order}')

part_one()