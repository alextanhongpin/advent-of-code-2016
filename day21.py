import re
import itertools

num_prog = re.compile(r'\d+')
alp_prog = re.compile(r'\s([a-z])\s')


def split(word: str) -> list[str]:
    return [ch for ch in word]


def scramble(ins: list[str], start: str) -> str:
    start = split(start)

    for line in ins:
        nums = [int(n) for n in num_prog.findall(line)]
        alps = [n for n in alp_prog.findall(line)]

        match line[:8]:
            case 'swap pos':
                x, y = nums
                start[x], start[y] = start[y], start[x]
            case 'swap let':
                x, y = alps
                xi, yi = start.index(x), start.index(y)
                start[xi], start[yi] = start[yi], start[xi]
            case 'rotate l':
                x = nums[0]
                while x > 0:
                    start.append(start.pop(0))
                    x -= 1
            case 'rotate r':
                x = nums[0]
                while x > 0:
                    start.insert(0, start.pop())
                    x -= 1
            case 'rotate b':
                x = alps[0]
                xi = start.index(x)
                if xi >= 4:
                    xi += 1
                xi += 1
                while xi > 0:
                    start.insert(0, start.pop())
                    xi -= 1
            case 'reverse ':
                xi, yi = nums
                for i in range((yi-xi)//2+1):
                    start[xi+i], start[yi-i] = start[yi-i], start[xi+i]
            case 'move pos':
                x, y = nums
                start.insert(y, start.pop(x))
            case _:
                raise ValueError(f'Unknown instruction: {line}')
        # print(line.strip(), ''.join(start))
    return ''.join(start)


with open('input.txt') as f:
    lines = f.readlines()
    scrambled = scramble(lines, 'abcdefgh')
    print('part 1:', scrambled)
    for per in itertools.permutations('abcdefgh'):
        if scramble(lines, per) == 'fbgdceah':
            print('part 2:', ''.join(per))

