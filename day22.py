import re
from collections import namedtuple
import copy
import heapq
from dataclasses import dataclass, field
from typing import Any


num_prog = re.compile(r'\d+')

DC = namedtuple('DC', 'id x y size used avail, used_percentage')
State = namedtuple('State', 'dc_id size_transferred')

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    x: int = field(compare=False)
    y: int = field(compare=False)
    steps: int = field(compare=False)
    state: Any=field(compare=False)


neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def bfs(dcs: list[DC]) -> int:
    q = []
    target = None
    dc_by_pos = {}
    max_size_by_dc = {}
    for dc in dcs:
        max_size_by_dc[(dc.x, dc.y)] = dc.size
        dc_by_pos[(dc.x, dc.y)] = State(dc.id, dc.used)
        if target is None or (dc.x > target.x and dc.y == 0):
            target = dc
    for dc in dcs:
        if dc.used == 0:
            q.append(PrioritizedItem(0, dc.x, dc.y, 0, dc_by_pos))

    if target is None:
        raise Exception('No target found')

    draw(dcs, target=(target.x, target.y), empty=(q[0].x, q[0].y), max_size=target.size)

    cache = set()

    epoch = 0
    while q:
        epoch += 1
        h = heapq.heappop(q)
        x, y, steps, dc_by_pos = h.x, h.y, h.steps, h.state

        if dc_by_pos[(0, 0)].dc_id == target.id:
            return steps

        key = frozenset(sorted((k, v.dc_id)
                               for k, v in dc_by_pos.items()))
        if key in cache:
            continue
        cache.add(key)
        print(epoch, steps, h.priority)
        # draw(dcs)

        empty = None
        dc_target = None
        for xy, dc in dc_by_pos.items():
            if dc.size_transferred == 0:
                empty = xy
            if dc.dc_id == target.id:
                dc_target = xy
            if empty is not None and dc_target is not None:
                break
        draw(dcs, target=dc_target, empty=empty, max_size=target.size)

        for dx, dy in neighbors:
            dx += x
            dy += y
            if (dx, dy) not in dc_by_pos:
                continue
            zero = dc_by_pos[(x, y)]
            curr = dc_by_pos[(dx, dy)]
            max_size = max_size_by_dc[(x, y)]

            dbp = copy.deepcopy(dc_by_pos)
            dbp[(x, y)] = curr
            dbp[(dx, dy)] = zero
            key = frozenset(sorted((k, v.dc_id)
                                   for k, v in dbp.items()))
            if key in cache:
                continue

            if curr.size_transferred <= max_size:
                dist = 0
                for k in dbp:
                    if dbp[k].dc_id == target.id:
                        # 5x the distance from target to 0, 0
                        dist += 5 * (abs(k[0]) + abs(k[1]))

                        # We need to overcome this barrier.
                        if dy > 21:
                            dist += abs(dx - 0) + abs(dy - 21)
                        # Distance from empty dc to target
                        dist += (abs(dx - k[0]) + abs(dy - k[1]))
                        break
                heapq.heappush(q, PrioritizedItem(dist, dx, dy, steps + 1, dbp))
            else:
                cache.add(key)
    return -1


def draw(dcs: list[DC], target=(0, 0), empty=(0, 0), max_size=0):
    max_x = max(dc.x for dc in dcs)
    max_y = max(dc.y for dc in dcs)

    dcs_by_pos = {}
    for dc in dcs:
        dcs_by_pos[(dc.x, dc.y)] = dc


    for y in range(max_y + 1):
        if y == 0:
            # Print the position vertically. Printing x from 0 to 11 is
            # 000000000011
            # 012345678901
            print(f'   ', end='')
            for x in range(max_x + 1):
                print(x//10, end='')
            print()
            print(f'   ', end='')
            for x in range(max_x + 1):
                print(x%10, end='')
            print()

        # Print the y position.
        print(f'{y:02d} ', end='')
        for x in range(max_x + 1):
            if x == 0 and y == 0:
                print('G', end='')
            elif x == empty[0] and y == empty[1]:
                print('_', end='')
                continue
            elif x == target[0] and y == target[1]:
                print('T', end='')
                continue
            else:
                curr = dcs_by_pos[(x, y)]
                if curr.used <= max_size:
                    print('.', end='')
                else:
                    print('#', end='')
        print()


with open('input.txt') as f:
    dcs = []
    for line in f:
        if not line.startswith('/dev'):
            continue
        dc_id = line.split(' ')[0]
        dc = DC(dc_id, *[int(x) for x in num_prog.findall(line)])
        dcs.append(dc)

    viable = set()
    for i, dc0 in enumerate(dcs):
        for j, dc1 in enumerate(dcs):
            if i == j:
                continue
            if dc0.used > 0 and dc0.used <= dc1.avail:
                viable.add(frozenset((dc0, dc1)))

    print('part 1:', len(viable))
    print('part 2:', bfs(dcs))
