

def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data

data = read_puzzle_data('Day_02_data.txt')
print(data)
