import datetime
import re


class LogEntry:
    def __init__(self, text_log_entry):
        result = re.search(r'^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)', text_log_entry)
        self.timestamp = datetime.datetime(int(result.group(1)), int(result.group(2)), int(result.group(3)),
                                           int(result.group(4)), int(result.group(5)))
        self.guard_id = 0
        self.entry_text = result.group(6)
        result = re.search('Guard #(\d+)', self.entry_text)
        if result:
            self.guard_id = result.group(1)

    def __repr__(self):
        return f'{self.timestamp} {self.entry_text} id: {self.guard_id}'

    def __lt__(self, other):
        return self.timestamp < other.timestamp


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data

def sort_log(text_log_entries):
    rval = []
    for text_log_entry in text_log_entries:
        rval.append(LogEntry(text_log_entry))
    rval.sort()
    return rval


def part_1():
    text_log_entries = read_puzzle_data('Day_04_short_data.txt')
    log = sort_log(text_log_entries)
    for entry in log:
        print(entry)

part_1()