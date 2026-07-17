import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

m2 = re.search(r'\{\/\* Section 2: Columns Partition Builder.*?\{\/\* Section 3:', content, flags=re.DOTALL)
if m2:
    print(m2.group(0))
