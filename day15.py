# Disc #1 has 13 positions; at time=0, it is at position 11.
# Disc #2 has 5 positions; at time=0, it is at position 0.
# Disc #3 has 17 positions; at time=0, it is at position 11.
# Disc #4 has 3 positions; at time=0, it is at position 0.
# Disc #5 has 7 positions; at time=0, it is at position 2.
# Disc #6 has 19 positions; at time=0, it is at position 17.
# Disc #7 has 11 positions; at time=0, it is at position 0.

t0 = 0

d1 = (11, 13)
d2 = (0, 5)
d3 = (11, 17)
d4 = (0, 3)
d5 = (2, 7)
d6 = (17, 19)
d7 = (0, 11)

p1_done = False

while True:
    d1_pos = (d1[0] + t0+1) % d1[1]
    d2_pos = (d2[0] + t0+2) % d2[1]
    d3_pos = (d3[0] + t0+3) % d3[1]
    d4_pos = (d4[0] + t0+4) % d4[1]
    d5_pos = (d5[0] + t0+5) % d5[1]
    d6_pos = (d6[0] + t0+6) % d6[1]
    d7_pos = (d7[0] + t0+7) % d7[1]

    if d1_pos == d2_pos == d3_pos == d4_pos == d5_pos == d6_pos == 0 and not p1_done:
        print('part 1:', t0)
        p1_done = True


    if d1_pos == d2_pos == d3_pos == d4_pos == d5_pos == d6_pos == d7_pos == 0:
        print('part 2:', t0)
        break
    t0 += 1
