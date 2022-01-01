from collections import deque, namedtuple

Elf = namedtuple('Elf', 'id')

n_elves = 3004953
elves = deque([Elf(i) for i in range(1, n_elves + 1)])

while len(elves) > 1:
    if len(elves) % 1e3 == 0:
        print(len(elves))

    elves.rotate(-1)
    left_elf = elves.popleft()


print('part 1:', elves)


i = 1
while i * 3 < n_elves:
    i *= 3

print('part 2', n_elves - i)
