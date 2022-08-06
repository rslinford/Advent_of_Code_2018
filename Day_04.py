import datetime
import re
import unittest
from enum import Enum


class Guard:
    def __init__(self, id):
        self.id = id
        self.most_recent_entry = None
        self.winks = datetime.timedelta(0) # total minutes slept

    def __repr__(self):
        return f'Guard({self.id}) winks: {self.winks}  current: {self.most_recent_entry}'

class Event(Enum):
    BEGINS_SHIFT = 1
    FALLS_ASLEEP = 2
    WAKES_UP = 3


class LogEntry:
    def __init__(self, text_log_entry):
        result = re.search(r'^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)', text_log_entry)
        self.timestamp = datetime.datetime(int(result.group(1)), int(result.group(2)), int(result.group(3)),
                                           int(result.group(4)), int(result.group(5)))
        self.guard_id = 0
        self.entry_text = result.group(6)
        result = re.search('Guard #(\d+)', self.entry_text)
        if result:
            self.guard_id = int(result.group(1))

        if self.entry_text.find('begins shift') != -1:
            self.event_type = Event.BEGINS_SHIFT
        elif self.entry_text.find('falls asleep') != -1:
            self.event_type = Event.FALLS_ASLEEP
        elif self.entry_text.find('wakes up') != -1:
            self.event_type = Event.WAKES_UP
        else:
            raise ValueError(f'Unrecognized event type {self.entry_text}')

    def __repr__(self):
        return f'{self.timestamp} {self.event_type} id: {self.guard_id}'

    def __lt__(self, other):
        return self.timestamp < other.timestamp

"""
000000000011111111112222222222333333333344444444445555555555
012345678901234567890123456789012345678901234567890123456789
"""

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

def grock_log(log):
    guard_pool = {}
    guard_on_duty = None
    for entry in log:
        if entry.guard_id:
            if entry.guard_id not in guard_pool.keys():
                guard_pool[entry.guard_id] = Guard(entry.guard_id)
            guard_on_duty = guard_pool[entry.guard_id]
            if guard_on_duty.most_recent_entry:
                pass # todo: state transition logic here: Changing of the Guard
            guard_on_duty.most_recent_entry = entry
            print(guard_on_duty)
        else:
            print(f'On duty {guard_on_duty}')
            if entry.event_type == Event.WAKES_UP:
                # The last event should be a Falls Asleep
                assert(guard_on_duty.most_recent_entry.event_type == Event.FALLS_ASLEEP)
                # Record those winks
                delta = entry.timestamp - guard_on_duty.most_recent_entry.timestamp
                guard_on_duty.winks += delta
                print(f'Delta {delta}')
            # todo: State transition logic here: Simple State Change
            guard_on_duty.most_recent_entry = entry



def part_1():
    text_log_entries = read_puzzle_data('Day_04_short_data.txt')
    log = sort_log(text_log_entries)
    grock_log(log)
    for entry in log:
        print(entry)

part_1()


class TestLog(unittest.TestCase):
    def test_log_entry(self):
        log = sort_log(read_puzzle_data('Day_04_short_data.txt'))

        self.assertTrue(log[0].__repr__().find('Event') != -1)
        self.assertEqual(10, log[0].guard_id)
        self.assertEqual(Event.BEGINS_SHIFT, log[0].event_type)
        self.assertEqual(datetime.datetime(1518, 11, 1, 0, 0),
                         log[0].timestamp)
        self.assertEqual(datetime.datetime(1518, 11, 1, 0, 5),
                         log[1].timestamp)
        self.assertNotEqual('', log[1].event_type, Event.BEGINS_SHIFT)