import re

prog = re.compile(r"\d+")


def is_triangle(sides: list[int]) -> bool:
    """
    >>> is_triangle([3, 4, 5])
    True
    >>> is_triangle([3, 4, 6])
    False
    """
    sides = sorted(sides)
    return sides[0] + sides[1] > sides[2]


with open('input.txt') as f:
    horizontal = 0
    vertical = 0
    lines = f.readlines()
    triangles = []
    for row, line in enumerate(lines):
        match = prog.findall(line)
        triangle = [int(x) for x in match]
        triangles.append(triangle)
        horizontal += is_triangle(triangle)

        if row > 0 and (row+1) % 3 == 0:
            parts = list(zip(*triangles[row-2:row+1]))
            vertical += sum(is_triangle(list(triangle)) for triangle in parts)

    print(f'part 1: {horizontal}')
    print(f'part 2: {vertical}')
