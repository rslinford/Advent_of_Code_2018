import unittest


class ScoreBoard:
    def __init__(self):
        self.scores = [3, 7]
        self.elves = [0, 1]

    def _elf_id_at(self, i):
        for j, elf in enumerate(self.elves):
            if i == elf:
                return j
        return None

    def advance_elves(self):
        for i, elf in enumerate(self.elves):
            self.elves[i] = (elf + 1 + self.scores[elf]) % len(self.scores)

    def __repr__(self):
        string = []
        for i, score in enumerate(self.scores):
            elf_id = self._elf_id_at(i)
            if elf_id is None:
                string.append(f'{score}')
            elif elf_id == 0:
                string.append(f'({score})')
            elif elf_id == 1:
                string.append(f'[{score}]')
            else:
                string.append(f'{score}')
        return ', '.join(string)

    def create_new_recipes(self):
        total = 0
        for elf in self.elves:
            total += self.scores[elf]
        for c in str(total):
            self.scores.append(int(c))

    def score_ten(self, puzzle_input):
        string = []
        for i in range(puzzle_input, puzzle_input + 10):
            string.append(f'{self.scores[i]}')
        return int(''.join(string))

    def last_five(self):
        if len(self.scores) < 5:
            return ''
        string = []
        for score in self.scores[-5:]:
            string.append(f'{score}')
        return ''.join(string)

def part_one(puzzle_input):
    sb = ScoreBoard()
    # print(sb)
    while len(sb.scores) < puzzle_input + 10:
        sb.create_new_recipes()
        sb.advance_elves()
        # print(sb)
    return sb.score_ten(puzzle_input)


def part_two(puzzle_input):
    sb = ScoreBoard()
    last_five = ''
    while last_five != puzzle_input:
        sb.create_new_recipes()
        sb.advance_elves()
        last_five = sb.last_five()
    return len(sb.scores) - 5


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one(607331))
        self.assertEqual(5158916779, part_one(9))
        self.assertEqual(9251071085, part_one(18))
        self.assertEqual(5941429882, part_one(2018))

    def test_part_two(self):
        self.assertEqual(-1, part_two('607331'))
        # self.ass/tEqual(2018, part_two('59414'))
