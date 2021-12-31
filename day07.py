def parse(inp: str) -> tuple[list[str], list[str]]:
    ins, out = [], []
    tmp = ''
    for ch in inp.strip():
        match ch:
            case '[':
                out.append(tmp)
                out.append('[')
                tmp = ''
            case ']':
                out.pop()
                ins.append(tmp)
                tmp = ''
            case _:
                tmp += ch
    if tmp != '':
        out.append(tmp)
    return ins, out


def is_abba(ip: str) -> bool:
    n = len(ip)
    for i in range(n - 3):
        a, b, c, d = ip[i:i+4]
        if a == d and b == c and a != b:
            return True
    return False

def has_tls(ins: list[str], out: list[str]) -> bool:
    return any(is_abba(ip) for ip in out) and all(not is_abba(ip) for ip in ins)


def is_aba(ip: str) -> list[tuple[str, str]]:
    n = len(ip)
    res = []
    for i in range(n - 2):
        a, b, c = ip[i:i+3]
        if a == c and a != b:
            res.append((a, b))
    return res

def has_ssl(ins: list[str], out: list[str]) -> bool:
    abas = set()
    for ip in out:
        aba = is_aba(ip)
        for t in aba:
            abas.add(t)
    for ip in ins:
        bab = is_aba(ip)
        for (b, a) in bab:
            if (a, b) in abas:
                return True
    return False

support_tls = 0
support_ssl = 0
with open('input.txt') as f:
    for line in f:
        ins, out = parse(line)
        support_tls += has_tls(ins, out)
        support_ssl += has_ssl(ins, out)

print(f'part 1: {support_tls}')
print(f'part 2: {support_ssl}')
