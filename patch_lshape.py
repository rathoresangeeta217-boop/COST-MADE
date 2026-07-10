import re

with open('src/pages/LShapeTableCalculator.tsx', 'r') as f:
    content = f.read()

# Declare topPerimeterM outside the if block
replacement = """
  let bCostTotal = topCost;

  let topPerimeterM = (mainWidth * 2 + mainDepth * 2) / 1000;
  if (includeReturnStorage) {
    topPerimeterM += (returnWidth * 2 + returnDepth * 2) / 1000;
    topPerimeterM -= (2 * Math.min(mainDepth, returnDepth)) / 1000;
  }
  topPerimeterM *= 1.2; // 20% wastage

  if (topMaterialCategory === "board" || topMaterialCategory === "mdf") {
"""
content = re.sub(
    r'  let bCostTotal = topCost;\n\n  if \(topMaterialCategory === "board" \|\| topMaterialCategory === "mdf"\) \{',
    replacement,
    content
)

# Remove the inner declaration
content = re.sub(
    r'    let topPerimeterM = \(mainWidth \* 2 \+ mainDepth \* 2\) / 1000;\n    if \(includeReturnStorage\) \{\n      topPerimeterM \+= \(returnWidth \* 2 \+ returnDepth \* 2\) / 1000;\n      // Subtract the overlap joint length \(times 2 because both edges are joined\)\n      topPerimeterM -= \(2 \* Math.min\(mainDepth, returnDepth\)\) / 1000;\n    \}\n    \n    topPerimeterM \*= 1.2; // 20% wastage\n',
    '',
    content
)

with open('src/pages/LShapeTableCalculator.tsx', 'w') as f:
    f.write(content)
