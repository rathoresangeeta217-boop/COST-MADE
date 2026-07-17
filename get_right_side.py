with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

depth = 0
for idx, line in enumerate(lines):
    if idx < 1482: continue
    
    if "<div" in line and "</div>" in line:
        pass
    elif "<div" in line:
        depth += 1
    elif "</div" in line:
        depth -= 1
        if depth == 0:
            print(f"Closed at line {idx+1}")
            print(lines[idx-2:idx+3])
            break
