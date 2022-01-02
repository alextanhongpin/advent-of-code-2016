target = 4 * 633

n = 1
while n < target:
    if n % 2 == 0:
        n = n * 2 + 1
    else:
        n *= 2
print(n - target)
