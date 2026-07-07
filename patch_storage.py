import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Add LPATTI_COST
if "const LPATTI_COST" not in content:
    content = content.replace("const PROFIT_PERCENTAGE = 0.25;", "const PROFIT_PERCENTAGE = 0.25;\nconst LPATTI_COST = 6;")

# In main calcData
old_support_legs = """    // Support legs
    hardware.push({
      label: "Adjustable Heavy Levelling Legs","""

new_support_legs = """    // Support legs
    hardware.push({
      label: "Adjustable Heavy Levelling Legs","""

old_main_hardware = """    // Support legs"""
new_main_hardware = """    // L Patti
    const topPerimeterM = (width * 2 + depth * 2) / 1000;
    const pattiQty = Math.ceil(topPerimeterM * 3.28084 * 2); // 2 L-Pattis per foot of top perimeter
    hardware.push({
      label: "L Patti",
      qty: pattiQty,
      unitPrice: LPATTI_COST,
      unit: "pcs",
      cost: pattiQty * LPATTI_COST,
    });

    // Support legs"""
content = content.replace(old_main_hardware, new_main_hardware)

# In drawerCalcData
old_drawer_hardware = """    if (drawerLock) {
      hardware.push({
        label: "Drawer Lock","""

new_drawer_hardware = """    // L Patti
    const drawerPerimeterM = (drawerWidth * 2 + drawerDepth * 2) / 1000;
    const drawerPattiQty = Math.ceil(drawerPerimeterM * 3.28084 * 2);
    hardware.push({
      label: "L Patti",
      qty: drawerPattiQty,
      unitPrice: LPATTI_COST,
      unit: "pcs",
      cost: drawerPattiQty * LPATTI_COST,
    });

    if (drawerLock) {
      hardware.push({
        label: "Drawer Lock","""
content = content.replace(old_drawer_hardware, new_drawer_hardware)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
