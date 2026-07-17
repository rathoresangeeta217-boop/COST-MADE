import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.read().splitlines()

start_idx = 0
for i, line in enumerate(lines):
    if '{activeTab === "storage" && (' in line:
        start_idx = i
        break

end_idx = 0
for i in range(start_idx, len(lines)):
    if '{activeTab === "drawer" && (' in line:
        end_idx = i
        break

open_count = 0
for i in range(start_idx, end_idx):
    line = lines[i]
    line = re.sub(r'\{/\*.*?\*/\}', '', line)
    
    o = line.count('{')
    c = line.count('}')
    open_count += o
    open_count -= c
    if open_count < 0:
        print(f"Negative balance at line {i+1}: {line}")
        print(f"Balance: {open_count}")

print(f"Final balance: {open_count}")
