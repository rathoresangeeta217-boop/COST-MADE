import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("const butterflyCost = numLegs * 2 * 12.5;\n      const accessoriesCost = bufferCost + nutCost + butterflyCost;", "const butterflyCost = numLegs * 2 * 12.5;\n      const clampCost = numLegs * 2 * 10;\n      const accessoriesCost = bufferCost + nutCost + butterflyCost + clampCost;")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
