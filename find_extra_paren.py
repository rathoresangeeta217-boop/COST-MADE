with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

balance = 0
in_str = False
str_char = ''
for i, c in enumerate(text):
    if c in ("'", '"', '`'):
        if not in_str:
            in_str = True
            str_char = c
        elif c == str_char:
            in_str = False
    
    if not in_str:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
            if balance < 0:
                print(f"Negative paren balance at index {i}, around context:")
                print(text[i-50:i+50])
                # Reset balance to keep finding them
                balance = 0
