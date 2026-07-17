import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

m = re.search(r'\{\/\* Section 1: Dimensions & Material Base \*\/.*?(?=\{\/\* Section 2: Columns Partition Builder)', content, flags=re.DOTALL)
if m:
    s = m.group(0)
    s = re.sub(r'\{/\*.*?\*/\}', '', s, flags=re.DOTALL)
    open_divs = len(re.findall(r'<div\b', s))
    close_divs = len(re.findall(r'</div\b', s))
    print(f"Section 1 -> Open divs: {open_divs}, Close divs: {close_divs}")
else:
    print("Could not find section 1")

m2 = re.search(r'\{\/\* Section 2: Columns Partition Builder.*?\{\/\* Section 3:', content, flags=re.DOTALL)
if m2:
    s = m2.group(0)
    s = re.sub(r'\{/\*.*?\*/\}', '', s, flags=re.DOTALL)
    open_divs = len(re.findall(r'<div\b', s))
    close_divs = len(re.findall(r'</div\b', s))
    print(f"Section 2 -> Open divs: {open_divs}, Close divs: {close_divs}")
