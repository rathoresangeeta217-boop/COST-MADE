import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

bad_block = """  } else {
      legCostTotal = legCount * 1800;
      legDesc = `${legCount}x Metal U-Shape Legs`;
  } else {"""

good_block = """  } else {"""

content = content.replace(bad_block, good_block)

# Also we need to make sure hardwareLegCost gets added to hardwareCostTotal
hardware_add = """  let hardwareDetails = [];
  let hardwareCostTotal = 0;"""

hardware_add_new = """  let hardwareDetails = [];
  let hardwareCostTotal = 0;

  if (hardwareLegCost > 0) {
      hardwareDetails.push({ label: hardwareLegDesc, cost: hardwareLegCost });
      hardwareCostTotal += hardwareLegCost;
  }"""

content = content.replace(hardware_add, hardware_add_new)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
