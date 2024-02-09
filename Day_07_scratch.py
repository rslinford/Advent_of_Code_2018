import re
from collections import defaultdict

inpstr = open('Day_07_data.txt').read()
lines = inpstr.splitlines()

pat = re.compile(r'([A-Z]) ')

pairs = map(pat.findall, lines)
depend = defaultdict(set)
allow = defaultdict(set)

for first, second in pairs:
    depend[second].add(first)
    allow[first].add(second)

availables = sorted(set(allow) - set(depend), reverse=True)
ordered = ''

# Part1
while availables:
    next_available = availables.pop()
    ordered += next_available
    for el in allow[next_available]:
        if all(dep in ordered for dep in depend[el]) and el not in availables:
            availables.append(el)

    availables.sort(reverse=True)

print(ordered)

# Part2

availables = sorted(set(allow) - set(depend), reverse=True)
done = []

workers = [{'remain': 0, 'task': None} for _ in range(5)]

t = -1
while availables or any(w['task'] is not None for w in workers):
    t += 1
    for w in workers:
        if w['task'] is not None and w['remain'] == 0:
            task = w['task']
            done.append(task)
            w['task'] = None
            for el in allow[task]:
                if all(dep in done for dep in depend[el]) and el not in availables:
                    availables.append(el)
            availables.sort(reverse=True)

        if w['remain'] == 0 and availables and w['task'] is None:
            next_available = availables.pop()
            reqtime = ord(next_available) - 4
            w['remain'] = reqtime
            w['task'] = next_available

        w['remain'] = max(0, w['remain'] - 1)

print(t)
