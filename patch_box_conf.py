import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """      } else if (legType === "box_plain") {
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

new_block = """      } else if (legType === "box_plain") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legName = `1x Open Box Base (Plain) (4 Panels: 2x ${boxWidth}mm W & 2x ${boxDepth}mm D x ${height}mm H, No Top/Bottom)`;
      } else if (legType === "box_fluted") {
          const boxWidth = Math.max(0, mainWidth - 600);
          const boxDepth = Math.max(0, mainDepth - 600);
          areaPerLegSqMm = (boxWidth * 2 + boxDepth * 2) * height;
          effectiveLegCount = 1;
          legRate += 100; // fluted premium
          legName = `1x Open Box Base (Fluted) (4 Panels: 2x ${boxWidth}mm W & 2x ${boxDepth}mm D x ${height}mm H, No Top/Bottom)`;
      }"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
