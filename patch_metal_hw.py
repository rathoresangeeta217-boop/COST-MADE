import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """    const hardwareCost = hardware.reduce((sum, h) => sum + h.cost, 0) + (constructionCategory === 'metal' ? totalHardwareCost : 0);"""

content = content.replace("    const hardwareCost = hardware.reduce((sum, h) => sum + h.cost, 0);", replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
