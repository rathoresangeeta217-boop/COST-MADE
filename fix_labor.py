import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_costs = """    const hwCost = hardware.reduce((sum, h) => sum + h.cost, 0);

    const netManufacturing = materialCost + hwCost + 3000 + 500 + 500;
    const profit = netManufacturing * 0.25;

    return {
      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: boardsSqFt,
        materialCost: materialCost,
        backingCost: 0,
        hardwareCost: hwCost,
        laborCost: 3000,
        packagingCost: 500,
        toolingCost: 500,"""

# Let's replace just line by line
content = content.replace("const netManufacturing = materialCost + hwCost + 3000 + 500 + 500;", 
    "const laborCost = Math.max(500, boardsSqFt * 40);\n    const packagingCost = Math.max(100, boardsSqFt * 15);\n    const toolingCost = Math.max(100, boardsSqFt * 10);\n\n    const netManufacturing = materialCost + hwCost + laborCost + packagingCost + toolingCost;")

content = content.replace("laborCost: 3000,", "laborCost,")
content = content.replace("packagingCost: 500,", "packagingCost,")
content = content.replace("toolingCost: 500,", "toolingCost,")

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
