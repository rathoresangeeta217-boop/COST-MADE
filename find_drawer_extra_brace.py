with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
lines = text.split('\n')[2530:2935]
fragment = '\n'.join(lines)
fragment = fragment.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

bal_b = 1 # Start with 1 because it starts with `{activeTab === "drawer" && (`
in_str, str_char = False, ''
for i, c in enumerate(fragment):
    if c in ("'", '"', '`'):
        if not in_str: in_str, str_char = True, c
        elif c == str_char: in_str = False
    
    if not in_str:
        if c == '{': bal_b += 1
        elif c == '}': 
            bal_b -= 1
            if bal_b == 0:
                print(f"Brace drops to 0 at index {i}, line {fragment[:i].count(chr(10)) + 2531}, context: {fragment[i-50:i+50]}")
