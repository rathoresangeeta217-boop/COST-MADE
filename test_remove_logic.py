import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'  const activeBoard =.*?return \(',
    '  return (',
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
