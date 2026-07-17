with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
lines = text.split('\n')[591:2528]
fragment = '\n'.join(lines)
fragment = fragment.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

c1, c2, b1, b2 = 0, 0, 0, 0
in_str, str_char = False, ''
for c in fragment:
    if c in ("'", '"', '`'):
        if not in_str: in_str, str_char = True, c
        elif c == str_char: in_str = False
    if not in_str:
        if c == '(': c1 += 1
        elif c == ')': c2 += 1
        elif c == '{': b1 += 1
        elif c == '}': b2 += 1
print(f"( = {c1}, ) = {c2}")
print(f"{{ = {b1}, }} = {b2}")
