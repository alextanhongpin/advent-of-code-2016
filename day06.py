from collections import Counter

with open('input.txt') as f:
    data = f.read().splitlines()
    part2 = ""
    print('part 1:', end=' ')
    for row in list(zip(*data)):
        counter = Counter(row)
        ch = counter.most_common(1)[0][0]
        print(ch, end='')
        part2 += counter.most_common()[-1][0][0]
    print()
    print("part 2:", part2)
