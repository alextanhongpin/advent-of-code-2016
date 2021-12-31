from collections import defaultdict
import re


prog = re.compile(r'\d+')

with open('input.txt') as f:
    ins = sorted([line.strip() for line in f], reverse=True)
    bots = defaultdict(list)
    outputs = defaultdict(list)
    processes = []
    cmp = defaultdict(int)

    for i in ins:
        if i.startswith('value'):
            v, bot = prog.findall(i)
            v, bot = int(v), int(bot)
            bots[bot].append(v)
        else:
            processes.append(i)

    while len(processes) > 0:
        i = processes.pop()
        bot, boto0, boto1 = [int(d) for d in prog.findall(i)]
        bots[bot].sort()
        if len(bots[bot]) < 2:
            processes.insert(0, i)
            continue

        lo, *rest, hi = bots[bot]
        bots[bot] = rest
        cmp[(lo, hi)] = bot

        if 'low to bot' in i:
            bots[boto0].append(lo)
        else:
            outputs[boto0].append(lo)

        if 'high to bot' in i:
            bots[boto1].append(hi)
        else:
            outputs[boto1].append(hi)

    print('part 1:', cmp[(17, 61)])
    print('part 2:', outputs[0][0] * outputs[1][0] * outputs[2][0])
