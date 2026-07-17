with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.readlines()

depth = 0
for idx, line in enumerate(lines):
    if idx < 592: continue # Line 593 is where {activeTab === "storage" && (<div className="grid grid-cols-1 ..."> begins
    if idx > 2578: break
    if "<div" in line and "</div>" in line:
        pass
    elif "<div" in line:
        depth += 1
    elif "</div" in line:
        depth -= 1

print(f"Final depth for storage tab: {depth}")
