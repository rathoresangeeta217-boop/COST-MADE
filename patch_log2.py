import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_log = """    const netManufacturing = materialCost + hwCost + laborCost + packagingCost + toolingCost;
    const profit = netManufacturing * 0.25;"""

new_log = """    const netManufacturing = materialCost + hwCost + laborCost + packagingCost + toolingCost;
    const profit = netManufacturing * 0.25;
    console.log(`calcData - angleThickness: ${angleThickness}, boardId: ${boardId}, materialCost: ${materialCost}, grandTotal: ${netManufacturing + profit}`);"""

content = content.replace(old_log, new_log)
with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
