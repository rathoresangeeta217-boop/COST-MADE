import re

with open('src/lib/downloadHardwarePdf.ts', 'r') as f:
    content = f.read()

content = content.replace('["Butterfly Brackets", "12.5"],', '["Butterfly Brackets", "12.5"],\n      ["Clamp (2 per leg)", "10"],')

with open('src/lib/downloadHardwarePdf.ts', 'w') as f:
    f.write(content)
