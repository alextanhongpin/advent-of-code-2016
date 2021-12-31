from collections import defaultdict

def decompress2(inp: str) -> dict[str, int]:
    d = defaultdict(int)
    res = ''
    j = 0
    for i in range(len(inp)):
        if i < j:
            continue
        if inp[i] == '(':
            for k in range(i+1, len(inp)):
                if inp[k] == ')':
                    j = k
                    break
            n, times = inp[i+1:j].split('x')
            n, times = int(n), int(times)
            j += 1
            d[inp[j:j+n]] = times
            j += n
        if i < j:
            continue
        res += inp[i]
    d[res] = 1
    return d


def decompress_iter(inp: str, recursive = False) -> int:
    total = 0
    for k, v in decompress2(inp).items():
        if '(' in k and recursive:
            total += decompress_iter(k, recursive) * v
        else:
            total += len(k) * v
    return total


with open('input.txt') as f:
    full = 0
    once = 0
    for line in f:
        line = line.strip()
        once += decompress_iter(line)
        full += decompress_iter(line, recursive=True)
    print(f'part 1: {once}')
    print(f'part 2: {full}')
