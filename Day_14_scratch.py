def generateRecipe():
  state = [3, 7]
  pos = [0, 1]
  for x in state:
    yield x
  for t in range(10000000000):
    score = [int(c) for c in str(state[pos[0]] + state[pos[1]])]
    state.extend(score)
    for i in range(2):
      pos[i] = (pos[i] + 1 + state[pos[i]]) % len(state)
    for x in score:
      yield x

num = 607331
targetNum = int(num)
targetList = list(map(int, str(num)))

arr = []
for i, x in enumerate(generateRecipe()):
  arr.append(x)
  if i + 1 - 10 == targetNum:
    print('Part1', ''.join(map(str, arr[-10:])))
  if arr[-len(targetList):] == targetList:
    print('Part2', i + 1 - len(targetList))
    break