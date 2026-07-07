import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """      } else if (legType === "box_plain") {
          areaPerLegSqMm = (400 * 4) * height; // 400x400 box
          legDesc = `${legCount}x Box Legs (Plain)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (400 * 4) * height;"""

new_block = """      } else if (legType === "box_plain") {
          areaPerLegSqMm = (600 * 4) * height; // 600x600 box
          legDesc = `${legCount}x Box Legs (Plain)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (600 * 4) * height;"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
