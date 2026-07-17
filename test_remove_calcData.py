import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'  const calcData = useMemo\(\(\) => \{.*?\n  \}, \[.*?\]\);',
    '  const calcData = { pieces: [], hardware: [], totals: { grandTotal: 0 }, bayWidth: 0 };',
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
