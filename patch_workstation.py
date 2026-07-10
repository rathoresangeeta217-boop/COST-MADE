import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """  let bCostTotal = topCost;

  const topPerimeterMPerPerson = ((width * 2 + depth * 2) / 1000) * 1.2;
  const topPerimeterM = topPerimeterMPerPerson * actualPersons;

  // Edge Banding for Table Top (only for Wood tops)
  if (topMaterialCategory !== "marble") {"""

content = re.sub(
    r'  let bCostTotal = topCost;\n\n  // Edge Banding for Table Top \(only for Wood tops\)\n  if \(topMaterialCategory !== "marble"\) \{',
    replacement,
    content
)

content = re.sub(
    r'    const topPerimeterMPerPerson = \(\(width \* 2 \+ depth \* 2\) / 1000\) \* 1\.2;\n    const topPerimeterM = topPerimeterMPerPerson \* actualPersons;\n',
    '',
    content
)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
