import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """      } else if (legType === "box_plain") {
          areaPerLegSqMm = (600 * 4) * height; // 600x600 box
          legName = `${legCount}x Box Legs (Plain) (4 panels of 600mm x ${height}mm)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (600 * 4) * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Box Legs (Fluted) (4 panels of 600mm x ${height}mm)`;
      }"""

new_block = """      } else if (legType === "box_plain") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legName = `1x Box Base (Plain) (${boxWidth}mm W x ${boxDepth}mm D x ${height}mm H)`;
      } else if (legType === "box_fluted") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legRate += 100; // fluted premium
          legName = `1x Box Base (Fluted) (${boxWidth}mm W x ${boxDepth}mm D x ${height}mm H)`;
      }"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
