import copy

MAX_IP = 2 ** 32

def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals = copy.deepcopy(intervals)
    intervals.sort()
    res = [intervals.pop(0)]
    while intervals:
        a0, a1 = res.pop()
        b0, b1 = intervals.pop(0)
        if b0 - a1 <= 1:
            res.append((min(a0, b0), max(a1, b1)))
        else:
            res.append((a0, a1))
            res.append((b0, b1))
            res.sort()
    return sorted(res)





with open('input.txt') as f:
    ips = []
    for line in f:
        nums = [int(s) for s in line.strip().split('-')]
        nums.sort()
        a, b = nums
        ips.append((a, b))

    while True:
        new_ips = merge_intervals(ips)
        if ips == new_ips:
            break
        ips = new_ips

    lowest_ip = ips[0][1]+1
    allowed_ip_ranges = MAX_IP
    for a, b in ips:
        allowed_ip_ranges -= b - a + 1

    print('part 1:', lowest_ip)
    print('part 2:', allowed_ip_ranges)
