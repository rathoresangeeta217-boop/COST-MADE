import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Remove useMemo for pieces
content = re.sub(
    r'  const pieces = useMemo\(\(\) => \{.*?\n  \}, \[.*?\]\);',
    '  const pieces = [];',
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
