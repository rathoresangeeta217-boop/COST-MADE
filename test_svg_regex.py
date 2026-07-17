import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

m = re.search(r'          \{\/\* Section 4: Live 2D Front View Vector Preview \*\/.*?<svg', content, flags=re.DOTALL)
if m:
    print("MATCHED:\n", m.group(0)[-100:])
else:
    print("NO MATCH")
