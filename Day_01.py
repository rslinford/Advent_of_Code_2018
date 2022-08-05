

def read_puzzle_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(int(line.strip()))
    return data


def part_1():
    data = read_puzzle_data('Day_01_short_data.txt')
    tally = 0
    for x in data:
        tally += x
        print(x)
    print(f'Sum {tally}')


def part_2():
    data = read_puzzle_data('Day_01_data.txt')
    freq = {}
    tally = 0
    while True:
        freq[tally] = 1
        for x in data:
            tally += x
            if tally in freq.keys():
                print(f'Duplicate frequency {tally}')
                return
            else:
                freq[tally] = 1
            print(x)
        print(f'Sum {tally}')

part_2()