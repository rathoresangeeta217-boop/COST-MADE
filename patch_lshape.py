import re

with open('src/pages/LShapeTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("const butterflyCost = numLegs * 2 * 12.5;\n    const accessoriesCost = bufferCost + nutCost + butterflyCost;", "const butterflyCost = numLegs * 2 * 12.5;\n    const clampCost = numLegs * 2 * 10;\n    const accessoriesCost = bufferCost + nutCost + butterflyCost + clampCost;")
content = content.replace('label: "Leg Accessories (Buffer, Nut, Butterfly)",', 'label: "Leg Accessories (Buffer, Nut, Butterfly, Clamp)",')
content = content.replace('unitPrice: 37, // 7 + 5 + (2 * 12.5)', 'unitPrice: 57, // 7 + 5 + (2 * 12.5) + (2 * 10)')

with open('src/pages/LShapeTableCalculator.tsx', 'w') as f:
    f.write(content)
