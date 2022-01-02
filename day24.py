from collections import namedtuple
import heapq

Point = namedtuple('Point', 'x y')
State = namedtuple('State', 'point steps')

neighbors = [
    Point(-1, 0),
    Point(0, -1),
    Point(1, 0),
    Point(0, 1)
]

def bfs(start: Point, target: Point, obstacles: set[Point]) -> int:
    queue = [State(start, 0)]
    cache = set()
    while queue:
        item, steps = queue.pop(0)
        if item == target:
            return steps
        if item in cache:
            continue
        cache.add(item)
        for neighbor in neighbors:
            new_point = Point(item.x + neighbor.x, item.y + neighbor.y)
            if new_point in obstacles:
                continue
            queue.append(State(new_point, steps + 1))
    return -1

def min_steps(points: dict[str, Point], obstacles: set[Point], return_to_origin=False) -> int:
    zero = points['0']
    if not return_to_origin:
        del points['0']
    queue = [(0, zero, [])]
    cache = {}

    while queue:
        steps, start, visited = heapq.heappop(queue)
        if len(visited) == len(points) and not return_to_origin:
            return steps
        if len(visited) == len(points) and return_to_origin and visited[-1] == '0':
            return steps

        for n, point in points.items():
            if n in visited:
                continue
            key = (start, point)
            if key not in cache:
                new_steps = bfs(start, point, obstacles)
                cache[(point, start)] = new_steps
                cache[(start, point)] = new_steps
            new_steps = cache[key]
            new_visited = visited.copy()
            new_visited.append(n)
            heapq.heappush(queue, (steps+new_steps, point, new_visited))

with open('input.txt') as f:
    obstacles = set()
    points = {}
    y = 0
    for line in f:
        line = line.strip()
        for x, char in enumerate(line):
            match char:
                case '#':
                    obstacles.add(Point(x, y))
                case ch if ch.isdigit():
                    points[char] = Point(x, y)
                case _:
                    pass
        y += 1
    print(min_steps(points.copy(), obstacles))
    print(min_steps(points.copy(), obstacles, True))
