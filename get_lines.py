with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "Right Side: Interactive" in line:
        start_idx = idx
        break

print("Start index:", start_idx)
print("Line at start_idx + 1098:", lines[start_idx + 1098].strip())
print("Line at start_idx + 1063:", lines[start_idx + 1063].strip())
print("Line at start_idx + 1062:", lines[start_idx + 1062].strip())
