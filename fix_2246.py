with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    lines = f.read().splitlines()

# Delete line 2246 (0-indexed 2245)
# wait, let me do this safely.

start = 2240
end = 2250
for i in range(start-1, end):
    print(f"{i+1}: {lines[i]}")

