import hashlib
import copy
salt = 'zpqevtbw'

keys = []
idx = 0


found = {}

key_streching = True

while len(keys) < 64:
    inp = (salt + str(idx)).encode('utf-8')
    h = hashlib.md5(inp).hexdigest()
    if key_streching:
        for i in range(2016):
            h = hashlib.md5(h.encode('utf-8')).hexdigest()
    # print(h)
    # breakpoint()

    for i in range(0, len(h)-4):
        r3, r5 = h[i:i+3], h[i:i+5]
        if r5 == h[i]*5:
            items = copy.deepcopy(found).items()
            for (pdix, (p3, phash)) in items:
                if p3 != r3:
                    continue
                if pdix not in found:
                    continue
                keys.append((pdix, phash))
                del found[pdix]

    count = 0
    for i in range(0, len(h)-2):
        r3 = h[i:i+3]
        if r3 == h[i]*3:
            found[idx] = (r3, h)
            count += 1
            break

    found = {k: v for k, v in found.items() if idx-k < 1000}
    idx += 1

print(len(keys))
keys = sorted(keys, key=lambda x: x[0])[:64]
print(len(keys))
print(keys[-1])
