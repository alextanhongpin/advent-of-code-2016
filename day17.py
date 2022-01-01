import hashlib
from collections import namedtuple


State = namedtuple('State', 'x y steps passcode')
Doors = namedtuple('Doors', 'up down left right')


doors = set('bcdef')
neighbors = [('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0)]

def get_doors(passcode: str) -> Doors:
    h = hashlib.md5(passcode.encode('utf-8')).hexdigest()
    return Doors(*[neighbors[i] if door in doors else None
                   for i, door in enumerate(h[:4])])


def bfs(passcode: str) -> tuple[str, str]:
    queue = [State(0, 0, '', passcode)]
    visited = set()
    min_steps, max_steps = None, None
    while queue:
        x, y, steps, passcode = queue.pop(0)
        if x == 3 and y == 3:
            if min_steps is None or len(steps) < len(min_steps):
                min_steps = steps
            if max_steps is None or len(steps) > len(max_steps):
                max_steps = steps
            continue
        if (x, y, steps) in visited:
            continue
        visited.add((x, y, steps))

        for door in get_doors(passcode):
            if door is None:
                continue
            direction, dx, dy = door
            dx += x
            dy += y
            if -1 < dx < 4 and -1 < dy < 4:
                queue.append(State(dx, dy, steps + direction, passcode + direction))
    return (min_steps, max_steps)


print(bfs('bwnlcvfs'))
