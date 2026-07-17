import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# simple check for < without >
tags = re.findall(r'<[a-zA-Z0-9]+[^>]*$', content, flags=re.MULTILINE)
for t in tags:
    print(f"Unclosed tag: {t}")
