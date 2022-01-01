# The python solution is too slow, see the day11.go version written in golang.

from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
import copy
import re

level_by_floors = {
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
}

prog = re.compile(r'The (\w+) floor contains')


def parse(inp: str) -> defaultdict:
    floors = defaultdict(set)
    for line in inp.splitlines():
        line = line.strip()
        line = line.replace('.', '').replace(' a ', '').replace('-', ' ')
        if 'nothing' in line:
            continue

        match = prog.match(line)
        if not match:
            raise Exception('no match')

        level = level_by_floors[match[1]]
        items = line[match.end(0):]
        items = re.split(r'and|,', items)
        items = [item.strip() for item in items if item.strip() != '']
        floors[level] = set(items)
    return floors


State = namedtuple('State', ['steps', 'floors', 'level'])

def is_microchip_fried(items: set[str]) -> bool:
    gens, mics = set(), set()
    for item in items:
        name, *rest, kind = item.split(' ')
        if kind == 'generator':  # Generator
            gens.add(name)
        else:
            mics.add(name)
    return len(gens) > 0 and len(mics - gens) > 0


def bfs(floors: defaultdict[int, set]) -> int:
    q = deque([State(0, floors, 1)])
    n = sum(len(floors[level]) for level in floors)

    cache = {}
    fried = {}
    def is_fried(items: set[str]) -> bool:
        key = frozenset(items)
        if key in fried:
            return fried[key]
        fried[key] = is_microchip_fried(items)
        return fried[key]


    epoch = 0
    while len(q) > 0:
        epoch += 1
        steps, floors, level = q.popleft()
        if level == 4 and len(floors[4]) == n:
            print('completed in ', epoch, ' steps')
            return steps

        key = frozenset((level, frozenset((k, frozenset(v))
                        for k, v in floors.items())))
        if key in cache:
            continue
        cache[key] = True

        if epoch % 1e5 == 0:
            print(f'{epoch}', steps)

        items = floors[level]
        if is_fried(items):
            continue

        possible_items = []
        iteritems = list(items)
        for i, lhs in enumerate(iteritems):
            for rhs in iteritems[i+1:]:
                possible_items.append(set([lhs, rhs]))
            possible_items.append(set([lhs]))

        for items in possible_items:
            if is_fried(items):
                continue
            # ̨Move down rules
            # - only allow one item to be moved down at a time
            # - if the floors below are empty, skip
            if level > 1 and len(items) == 1:
                items_below_floor = 0
                for i in range(1, level):
                    items_below_floor += len(floors[i])
                if items_below_floor > 0:
                    new_floors = copy.deepcopy(floors)
                    new_floors[level - 1] |= items
                    new_floors[level] -= items

                    key = frozenset((level-1, frozenset((k, frozenset(v))
                                    for k, v in new_floors.items())))
                    if not is_fried(new_floors[level - 1]) and not is_fried(new_floors[level]) and key not in cache:
                        q.append(State(steps + 1, new_floors, level - 1))
            if level < 4 and len(items) == 2:
                new_floors = copy.deepcopy(floors)
                new_floors[level + 1] |= items
                new_floors[level] -= items

                key = frozenset((level+1, frozenset((k, frozenset(v))
                                for k, v in new_floors.items())))
                if not is_fried(new_floors[level + 1]) and not is_fried(new_floors[level]) and key not in cache:
                    q.append(State(steps + 1, new_floors, level + 1))

    return -1



with open('input.txt') as f:
    floors = parse(f.read())
    print('part 1:', bfs(floors))

    new_floors = copy.deepcopy(floors)
    new_floors[1] |= set(['elerium generator',
                          'elerium compatible microchip',
                          'dilithium generator',
                          'dilithium compatible microchip'])
    print('part 2:', bfs(new_floors))
