pos = [-1, 0, 1]

def safe_tiles(grid: str, n: int) -> int:
    n_safe_tiles = 0
    while n > 0:
        n_safe_tiles += grid.count('.')
        row = grid
        rng = range(len(row))
        new_row = ''
        for i, ch in enumerate(row):
            pos_sum = [i+p for p in pos]
            neighbors = ''.join([row[i] if i in rng else '.' for i in pos_sum])
            match neighbors:
                case '^^.' | '.^^' | '^..' | '..^':
                    new_row += '^'
                case _:
                    new_row += '.'
        grid = new_row
        n -= 1
    return n_safe_tiles


grid = '^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^.......'
print('part 1:', safe_tiles(grid, 40))
print('part 2:', safe_tiles(grid, 400_000))
