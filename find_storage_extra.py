with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
lines = text.split('\n')[591:2528]
fragment = '\n'.join(lines)
fragment = fragment.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

bal_p, bal_b = 1, 1 # Start with 1 because it starts with `{activeTab === "storage" && (`
in_str, str_char = False, ''
for i, c in enumerate(fragment):
    if c in ("'", '"', '`'):
        if not in_str: in_str, str_char = True, c
        elif c == str_char: in_str = False
    
    if not in_str:
        if c == '(': bal_p += 1
        elif c == ')': 
            bal_p -= 1
            if bal_p == 0:
                print(f"Paren drops to 0 at index {i}, context: {fragment[i-50:i+50]}")
        elif c == '{': bal_b += 1
        elif c == '}': 
            bal_b -= 1
            if bal_b == 0:
                print(f"Brace drops to 0 at index {i}, context: {fragment[i-50:i+50]}")
