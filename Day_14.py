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

    def __repr__(self):
        string = []
        for i, score in enumerate(self.scores):
            elf_id = self._elf_id_at(i)
            if elf_id is None:
                string.append(str(score))
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


def part_one(puzzle_input):
    sb = ScoreBoard()
    sb.create_new_recipes()
    return -1


def part_two(puzzle_input):
    return -1


class Test(unittest.TestCase):
    def test_part_one(self):
        # self.assertEqual(-1, part_one(607331))
        self.assertEqual(5158916779, part_one(9))

    def test_part_two(self):
        self.assertEqual(-1, part_two(-1))
        self.assertEqual(-1, part_two(-1))
