import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data

def count_letters(word):
    counts = {}
    for c in word:
        if c in counts.keys():
            counts[c] += 1
        else:
            counts[c] = 1
    return counts


def part_01(filename):
    data = read_puzzle_data(filename)
    twos_tally, threes_tally = 0, 0

    for s in data:
        counts = count_letters(s)
        for count in counts.values():
            if count == 2:
                twos_tally += 1
                break
        for count in counts.values():
            if count == 3:
                threes_tally += 1
                break
    return twos_tally * threes_tally

# Assumes that both are the same length
def differs_by_exactly_one(w1, w2):
    difference_count = 0
    for i in range(len(w1)):
        if w1[i] != w2[i]:
            difference_count += 1
            if difference_count > 1:
                return False
    return difference_count == 1

def extract_letters_in_common(w1, w2) :
    rval = []
    for i in range(len(w1)):
        if w1[i] == w2[i]:
            rval.append(w1[i])
    return ''.join(rval)

def part_02(filename):
    data = read_puzzle_data(filename)
    for w1 in data:
        for w2 in data:
            # print(w1, w2, differs_by_exactly_one(w1, w2))
            if differs_by_exactly_one(w1, w2):
                print(f'Letters in common: {extract_letters_in_common(w1, w2)}')
                return extract_letters_in_common(w1, w2)


result = part_02('Day_02_data.txt')
print(result)

class Test(unittest.TestCase):
    def test_part_01(self):
        result = part_01('Day_02_short_data.txt')
        self.assertEqual(12, result)

    def test_part_02(self):
        result = part_02('Day_02_short_data.txt')
        self.assertEqual('abcde', result)
