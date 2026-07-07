import re

with open('/app/applet/src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      if (legType === "board") {
          areaPerLegSqMm = (mainDepth - 200) * height; // simple slab
          legDesc = `${legCount}x Board Slab Legs`;
      } else if (legType === "box_plain") {"""

new_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      let effectiveLegCount = legCount;

      if (legType === "board") {
          areaPerLegSqMm = mainDepth * height;
          effectiveLegCount = 2;
          legDesc = `2x Board Slab Legs`;
      } else if (legType === "box_plain") {"""

content = content.replace(old_block, new_block)

old_block2 = """          legDesc = `${legCount}x Round Legs (Fluted)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * legCount) / 90000;
      legCostTotal = totalLegAreaSqFt * legRate;
  }"""

new_block2 = """          legDesc = `${legCount}x Round Legs (Fluted)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * effectiveLegCount) / 90000;
      legCostTotal = totalLegAreaSqFt * legRate;
  }"""

content = content.replace(old_block2, new_block2)

with open('/app/applet/src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
