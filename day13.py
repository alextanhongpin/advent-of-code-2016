inp = 1352
target = (31, 39)

def is_wall(x, y):
    # Hidden rule?
    if x < 0 or y < 0:
        return True
    total = x*x + 3*x + 2*x*y + y + y*y + inp
    return total.bit_count() % 2 == 1


def draw(x0, y0):
    for y in range(-10, y0):
        for x in range(-10, x0):
            if is_wall(x, y):
                print('#', end='')
            else:
                print('.', end='')
        print()

# draw(target[0], target[1])

neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def bfs(start, target):
    queue = [(0, start)]
    visited = set()

    obstacles = {}
    def is_obstacle(point):
        if point not in obstacles:
            obstacles[point] = is_wall(point[0], point[1])
        return obstacles[point]

    covered = set()
    while queue:
        (steps, current) = queue.pop(0)
        if steps <= 50:
            covered.add(current)
        if current == target:
            return steps, len(covered)
        if current in visited:
            continue
        visited.add(current)

        for (x, y) in neighbors:
            new_point = (current[0] + x, current[1] + y)
            if is_obstacle(new_point):
                continue
            queue.append((steps + 1, new_point))
    return None, None

print('part 1', bfs((1, 1), target))
