with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

depth = 0
for idx, line in enumerate(lines):
    if idx < 1483: continue
    if idx > 2483: break
    
    # naive parsing again
    if "<div" in line and "</div>" in line:
        pass
    elif "<div" in line:
        depth += 1
        print(f"{idx+1} + {depth}")
    elif "</div" in line:
        depth -= 1
        print(f"{idx+1} - {depth}")
