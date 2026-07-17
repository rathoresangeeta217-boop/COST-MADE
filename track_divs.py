with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

depth = 0
for idx, line in enumerate(lines):
    # This is a naive count, it might fail on multiple divs on one line but it's a good start
    if "<div" in line and "</div>" in line:
        pass # self contained, usually no net change unless it's complex
    elif "<div" in line:
        depth += 1
        if "xl:col-span-5" in line:
            print(f"Start right side at line {idx+1}, depth {depth}")
            target_depth = depth
    elif "</div" in line:
        if 'target_depth' in locals() and depth == target_depth:
            print(f"End right side at line {idx+1}, depth {depth}")
            del target_depth
        depth -= 1
