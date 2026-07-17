with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

depth = 0
for idx, line in enumerate(lines):
    if idx < 1400: continue
    if "<div" in line and "</div>" in line:
        pass 
    elif "<div" in line:
        depth += 1
        print(f"{idx+1}: + div (depth {depth}) - {line.strip()[:40]}")
    elif "</div" in line:
        print(f"{idx+1}: - div (depth {depth}) - {line.strip()[:40]}")
        depth -= 1
        if depth <= -2:
            break
