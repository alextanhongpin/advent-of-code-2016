from collections import Counter

with open('input.txt') as f:
    data = f.read().splitlines()
    p1, p2 = "", ""
    for row in list(zip(*data)):
        counter = Counter(row)
        p1 += counter.most_common(1)[0][0]
        p2 += counter.most_common()[-1][0][0]
    print("part 1:", p1)
    print("part 2:", p2)
