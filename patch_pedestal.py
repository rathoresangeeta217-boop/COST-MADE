import re

with open('src/pages/PedestalCalculator.tsx', 'r') as f:
    content = f.read()

# Add LPATTI_COST
if "const LPATTI_COST" not in content:
    content = content.replace("const PROFIT_PERCENTAGE = 0.25;", "const PROFIT_PERCENTAGE = 0.25;\nconst LPATTI_COST = 6;")

old_hardware = """  pieces.forEach((p) => {
    if (p.ebMm && p.ebMm > 0) {"""

new_hardware = """  const topPerimeterM = (width * 2 + depth * 2) / 1000;
  const pattiQty = Math.ceil(topPerimeterM * 3.28084 * 2); // 2 L-Pattis per foot of top perimeter
  hCost += pattiQty * LPATTI_COST;
  hardwareDetails.push({
    label: "L Patti",
    qty: pattiQty,
    unitPrice: LPATTI_COST,
    unitLabel: "pcs",
    cost: pattiQty * LPATTI_COST,
  });

  pieces.forEach((p) => {
    if (p.ebMm && p.ebMm > 0) {"""
content = content.replace(old_hardware, new_hardware)

with open('src/pages/PedestalCalculator.tsx', 'w') as f:
    f.write(content)
