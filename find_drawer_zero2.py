with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
lines = text.split('\n')[2530:2935]
fragment = '\n'.join(lines)
fragment = fragment.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

balance = 0
in_str, str_char = False, ''
for i, c in enumerate(fragment):
    if c in ("'", '"', '`'):
        if not in_str: in_str, str_char = True, c
        elif c == str_char: in_str = False
    
    if not in_str:
        if c == '(': balance += 1
        elif c == ')': 
            balance -= 1
            if balance == -1:
                print(f"Balance hit -1 at index {i}, context:")
                print(fragment[i-50:i+50])
