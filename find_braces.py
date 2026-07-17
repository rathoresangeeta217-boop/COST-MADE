with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

text = text.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

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
        if c == '{':
            balance += 1
        elif c == '}':
            balance -= 1
            if balance < 0:
                print(f"Negative brace balance at index {i}, around context:")
                print(text[i-50:i+50])
                balance = 0
                
print("Final brace balance:", balance)
