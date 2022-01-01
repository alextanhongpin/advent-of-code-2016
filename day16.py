def split(word: str) -> list[str]:
    return [char for char in word]


def reverse_flip(inp: str) -> str:
    res = ['1' if n == '0' else '0' for n in inp]
    res.append('0')
    res.append(inp)
    res.reverse()
    return ''.join(res)


def generate_checksum(inp: str) -> str:
    num = split(inp)
    while len(num) % 2 == 0:
        j = 0
        for i in range(0, len(num), 2):
            num[j] = str(int(num[i] == num[i + 1]))
            j += 1
        num = num[:len(num)//2]
    return ''.join(num)


def checksum(inp: str, length: int) -> str:
    while len(inp) < length:
        inp = reverse_flip(inp)
    return generate_checksum(inp[:length])


print(checksum('01111001100111011', 272))
print(checksum('01111001100111011', 35651584))
