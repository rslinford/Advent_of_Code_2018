inpstr = open('Day_08_data.txt').read()
inp = [int(n) for n in inpstr.split()]

acc = 0


def create_tree(L):
    global acc
    nchild = L[0]
    len_meta = L[1]

    if nchild == 0:
        metadata = L[2:2 + len_meta]
        acc += sum(metadata)
        return {'children': [], 'metadata': metadata, 'val': sum(metadata)}, L[2 + len_meta:]
    children = []
    L = L[2:]
    for _ in range(nchild):
        c, L = create_tree(L)
        children.append(c)
    metadata = L[:len_meta]
    acc += sum(metadata)
    val = sum(children[i - 1]['val'] for i in metadata if 0 < i <= len(children))
    return {'children': children, 'metadata': L[:len_meta], 'val': val}, L[len_meta:]


tree = create_tree(inp)

# Part 1
print(acc)

# Part2
val = tree[0]['val']
print(val)
