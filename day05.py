import hashlib


door_id = 'uqwqemis'
pwd = ""
i = 0

while len(pwd) != 8:
    result = hashlib.md5(str.encode(door_id + str(i)))
    digest = result.hexdigest()
    if digest.startswith('00000'):
        pwd += digest[5]
    i += 1

print(f'part 1: {pwd}')

pwd = ['_'] * 8
i = 0

while any(ch == '_' for ch in pwd):
    result = hashlib.md5(str.encode(door_id + str(i)))
    digest = result.hexdigest()
    if digest.startswith('00000'):
        pos = int(digest[5], 16)
        if pos < 8 and pwd[pos] == '_':
            pwd[pos] = digest[6]
            print(''.join(pwd))
    i += 1

print(f"part 2: {''.join(pwd)}")
