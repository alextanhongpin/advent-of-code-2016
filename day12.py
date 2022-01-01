
reg = [0, 0, 0, 0]
part2 = True
if part2:
    reg[2] = 1

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
        match line[:3]:
            case 'cpy':
                a, b = line[4:].split(' ')
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
                a, b = parse(a, True), parse(b)
                if a != 0:
                    offset += b
                    continue
            case _:
                print('unknown', line)
        offset += 1
    print('part 1:',reg[0])
