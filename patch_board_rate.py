import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "<option key={b.id} value={b.id}>{b.name}</option>",
    "<option key={b.id} value={b.id}>{b.name} (₹{getTopRate(b.id, b.costPerSqFt, topThickness, quality)}/sq.ft)</option>"
)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content2 = f.read()

content2 = content2.replace(
    "<option key={b.id} value={b.id}>{b.name}</option>",
    "<option key={b.id} value={b.id}>{b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)</option>"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content2)
