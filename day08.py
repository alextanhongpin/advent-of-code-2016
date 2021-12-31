import re

prog = re.compile(r'\d+')


def swipe(ops: str, width: int, height: int):
    screen = {(x, y): False for x in range(width)
              for y in range(height)}

    for op in ops.splitlines():
        a, b = [int(d) for d in prog.findall(op)]
        match op:
            case op if op.startswith('rect'):
                for y in range(b):
                    for x in range(a):
                        screen[x, y] = True
            case op if op.startswith('rotate row y'):
                new_row = {}
                for x in range(width):
                    new_row[(x+b) % width, a] = screen[x, a]
                    del screen[x, a]
                for x, y in new_row:
                    screen[x, y] = new_row[x, y]
            case op if op.startswith('rotate column x'):
                new_col = {}
                for y in range(height):
                    new_col[a, (y+b) % height] = screen[a, y]
                    del screen[a, y]
                for x, y in new_col:
                    screen[x, y] = new_col[x, y]

    for y in range(height):
        for x in range(width):
            print('#' if screen[x, y] else '.', end='')
        print()

    return sum(screen.values())


with open('input.txt') as f:
    ops = f.read()
    print(swipe(ops, 50, 6))
