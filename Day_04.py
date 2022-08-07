import datetime
import re
import unittest
from enum import Enum

import numpy as np


class Guard:
    def __init__(self, id):
        self.id = id
        self.most_recent_entry = None
        self.winks = datetime.timedelta(0)  # total minutes slept
        self.minute_tally = None

    def __repr__(self):
        return f'Guard({self.id}) winks: {self.winks}  current: {self.most_recent_entry}'

    def __lt__(self, other):
        return self.winks < other.winks


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


def mark_the_minutes(ts1: datetime.datetime, ts2: datetime.datetime, minute_tally):
    start_minute = ts1.minute
    end_minute = ts2.minute
    for minute in range(start_minute, end_minute):
        minute_tally[minute] += 1


def find_max_minute(minute_tally):
    max_minute = 0
    max_index = -1
    for i in range(minute_tally.shape[0]):
        if minute_tally[i] > max_minute:
            max_minute = minute_tally[i]
            max_index = i
    return max_index


def find_sleepiest_minute(guard, log):
    on_duty_guard_id = None
    minute_tally = np.zeros((60), dtype=int)
    for entry in log:
        if entry.guard_id:
            on_duty_guard_id = entry.guard_id
        else:
            if on_duty_guard_id == guard.id:
                if entry.event_type == Event.FALLS_ASLEEP:
                    guard.most_recent_entry = entry
                elif entry.event_type == Event.WAKES_UP:
                    assert (guard.most_recent_entry.event_type == Event.FALLS_ASLEEP)
                    delta = entry.timestamp - guard.most_recent_entry.timestamp
                    mark_the_minutes(guard.most_recent_entry.timestamp, entry.timestamp, minute_tally)
                else:
                    raise TypeError(f'Unexpected event type {entry.event_type}')
    return find_max_minute(minute_tally)


# Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?
def grok_log_strategy_one(log):
    guard_pool = {}
    guard_on_duty = None
    for entry in log:
        if entry.guard_id:
            if entry.guard_id not in guard_pool.keys():
                guard_pool[entry.guard_id] = Guard(entry.guard_id)
            guard_on_duty = guard_pool[entry.guard_id]
            if guard_on_duty.most_recent_entry:
                pass  # State transition logic here: Changing of the Guard
            guard_on_duty.most_recent_entry = entry
        else:
            if entry.event_type == Event.WAKES_UP:
                # The previous event should be a Falls Asleep
                assert (guard_on_duty.most_recent_entry.event_type == Event.FALLS_ASLEEP)
                # State transition logic: Simple State Change (same guard)
                # Record those winks
                delta = entry.timestamp - guard_on_duty.most_recent_entry.timestamp
                guard_on_duty.winks += delta
            guard_on_duty.most_recent_entry = entry
    guard_ranking = list(guard_pool.values())
    guard_ranking.sort(reverse=True)
    winner = guard_ranking[0]
    minute = find_sleepiest_minute(winner, log)
    return winner, minute

def find_minute_of_greatest_frequency(guard_pool):
    greatest_max_minute = 0
    greatest_guard = None
    greatest_max_index = 0
    for guard in guard_pool.values():
        max_minute_index = find_max_minute(guard.minute_tally)
        print(f'Minute: {max_minute_index} Tallied at: {guard.minute_tally[max_minute_index]} for\n{guard.minute_tally}')
        if guard.minute_tally[max_minute_index] > greatest_max_minute:
            greatest_max_minute = guard.minute_tally[max_minute_index]
            greatest_guard = guard
            greatest_max_index = max_minute_index
    return greatest_guard, greatest_max_index

def find_sleepiest_minute_two(guard_pool, log):
    for guard in guard_pool.values():
        on_duty_guard_id = None
        guard.minute_tally = np.zeros((60), dtype=int)
        for entry in log:
            if entry.guard_id:
                on_duty_guard_id = entry.guard_id
            else:
                if on_duty_guard_id == guard.id:
                    if entry.event_type == Event.FALLS_ASLEEP:
                        guard.most_recent_entry = entry
                    elif entry.event_type == Event.WAKES_UP:
                        assert (guard.most_recent_entry.event_type == Event.FALLS_ASLEEP)
                        mark_the_minutes(guard.most_recent_entry.timestamp, entry.timestamp, guard.minute_tally)
                    else:
                        raise TypeError(f'Unexpected event type {entry.event_type}')

    return find_minute_of_greatest_frequency(guard_pool)


# Of all guards, which guard is most frequently asleep on the same minute?
def grok_log_strategy_two(log):
    guard_pool = {}
    guard_on_duty = None
    for entry in log:
        if entry.guard_id:
            if entry.guard_id not in guard_pool.keys():
                guard_pool[entry.guard_id] = Guard(entry.guard_id)
            guard_on_duty = guard_pool[entry.guard_id]
            if guard_on_duty.most_recent_entry:
                pass  # State transition logic here: Changing of the Guard
            guard_on_duty.most_recent_entry = entry
        else:
            if entry.event_type == Event.WAKES_UP:
                # The previous event should be a Falls Asleep
                assert (guard_on_duty.most_recent_entry.event_type == Event.FALLS_ASLEEP)
                # State transition logic: Simple State Change (same guard)
                # Record those winks
                delta = entry.timestamp - guard_on_duty.most_recent_entry.timestamp
                guard_on_duty.winks += delta
            guard_on_duty.most_recent_entry = entry

    winner, minute = find_sleepiest_minute_two(guard_pool, log)
    return winner, minute


def part_one(filename):
    text_log_entries = read_puzzle_data(filename)
    log = sort_log(text_log_entries)
    winner, minute = grok_log_strategy_one(log)
    # for entry in log:
    #     print(entry)
    return winner, minute


def part_two(filename):
    text_log_entries = read_puzzle_data(filename)
    log = sort_log(text_log_entries)
    winner, minute = grok_log_strategy_two(log)
    print(f'Greatest minute {minute} for {winner}')
    return winner, minute


winner, minute = part_two('Day_04_data.txt')
print(f'Winner: {winner.id} minute: {minute} answer: {winner.id * minute}')


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

    def test_part_1(self):
        winner, minute = part_one('Day_04_short_data.txt')
        self.assertEqual(10, winner.id)
        self.assertEqual(24, minute)
