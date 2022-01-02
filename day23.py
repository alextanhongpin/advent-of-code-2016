import math
reg = [0, 0, 0, 0]
reg[0] = 7
print(f"part 2: {math.factorial(12) + 79 * 97}")

def parse(a: str, is_reg = False) -> int:
    a = a.strip()
    if a.isalpha():
        idx = ord(a) - ord('a')
        return reg[idx] if is_reg else idx
    else:
        return int(a)

with open('input.txt') as f:
    lines = f.readlines()
    offset = 0
    while True:
        if offset >= len(lines):
            break
        line = lines[offset].strip()
        # print(reg, line)
        match line[:3]:
            case 'cpy':
                a, b = line[4:].split(' ')
                if b.isdigit():
                    continue
                a, b = parse(a, True), parse(b)
                reg[b] = a
            case 'inc':
                a = parse(line[4:])
                reg[a] += 1
            case 'dec':
                a = parse(line[4:])
                reg[a] -= 1
            case 'jnz':
                a, b = line[4:].split(' ')
                a, b = parse(a, True), parse(b, b.isalpha())
                if a != 0:
                    offset += b
                    continue
            case 'tgl':
                a = parse(line[4:], True)
                if -1 < offset + a < len(lines):
                    line = lines[offset + a].strip()
                    match line[:3]:
                        case 'inc':
                            lines[offset + a] = 'dec ' + line[4:]
                        case 'dec':
                            lines[offset + a] = 'inc ' + line[4:]
                        case 'jnz':
                            lines[offset + a] = 'cpy ' + line[4:]
                        case 'cpy':
                            lines[offset + a] = 'jnz ' + line[4:]
                        case 'tgl':
                            lines[offset + a] = 'inc ' + line[4:]
                        case _:
                            print('Unknown instruction:', line)
            case _:
                print('unknown', line)
        offset += 1
    print('part 1:',reg[0])
