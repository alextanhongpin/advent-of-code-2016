from collections import Counter


def valid_checksum(inp: str) -> tuple[int, bool]:
    parts = inp.split('-')
    id_checksum = parts.pop()
    id, checksum = id_checksum[:-1].split('[')
    counter = Counter(''.join(parts))

    freq = counter.most_common(1)[0][1]

    # There can be multiple most common letters, so we need to check all of
    # them.
    most_common = set()
    for k, v in counter.items():
        if v == freq:
            most_common.add(k)
    if checksum[0] not in most_common:
        return 0, False

    for i in range(1, len(checksum)):
        prev, curr = checksum[i-1], checksum[i]
        if prev not in counter or curr not in counter:
            return 0, False
        if counter[prev] < counter[curr]:
            return 0, False

    return int(id), True


inp = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

def decode(cipher: str, n: int) -> str:
    def rotate(c: str) -> str:
        if c == '-':
            return ' '
        ch = ord(c) - ord('a') + n
        ch = ch % 26
        ch = ch + ord('a')
        return chr(ch)

    return str(''.join([rotate(ch) for ch in cipher]))


with open('input.txt', 'r') as f:
    total = 0
    # for line in inp.splitlines():
    for line in f:
        id, valid = valid_checksum(line.strip())
        if valid:
            total += id
            decoded = decode(line.strip(), id)
            if 'north' in decoded:
                print('part 2:', id, decoded)
    print('part 1:', total)
