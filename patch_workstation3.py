import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_args = """  sideScreenCoverage = "full",
  includeModesty,
  modestyType = "standard",
  modestyFinish = "plain",
  cncDesignOnModesty = false,
  wireManagement,
  includePedestal,"""
new_args = """  sideScreenCoverage = "full",
  includeModesty,
  modestyType = "standard",
  modestyFinish = "plain",
  cncDesignOnModesty = false,
  wireManagement,
  flapBoxRate = 450,
  includePedestal,"""
content = content.replace(old_args, new_args)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
