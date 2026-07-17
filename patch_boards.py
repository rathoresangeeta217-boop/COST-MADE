import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("BOARDS.find", "boards.find")

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
