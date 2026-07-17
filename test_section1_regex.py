import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

m = re.search(r'            \{\/\* Board Material and Thickness Selection \*\/.*?<\/div>\n            <\/div>', content, flags=re.DOTALL)
if m:
    print("MATCHED:\n", m.group(0))
else:
    print("NO MATCH")
