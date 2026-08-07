import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_thicknesses = """  if (boardId === "slotted_angle") {
    return [0.6, 0.8, 1, 1.2, 1.6, 2];
  }"""
new_thicknesses = """  if (boardId === "slotted_angle") {
    return [1.2, 1.6, 2.0, 2.5, 3.0];
  }"""
content = content.replace(old_thicknesses, new_thicknesses)

old_rates = """    if (boardId === "slotted_angle") {
        if (numThk === 2) return 125;
        if (numThk === 1.6) return 96;
        if (numThk === 1.2) return 72;
        if (numThk === 1) return 62;
        if (numThk === 0.8) return 52;
        if (numThk === 0.6) return 41;
        return baseRate;
    }"""
new_rates = """    if (boardId === "slotted_angle") {
        if (numThk === 3.0) return 110;
        if (numThk === 2.5) return 90;
        if (numThk === 2.0) return 75;
        if (numThk === 1.6) return 60;
        if (numThk === 1.2) return 45;
        return baseRate;
    }"""
content = content.replace(old_rates, new_rates)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
