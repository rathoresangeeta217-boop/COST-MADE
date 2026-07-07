import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """      if (legType === "board") {
          const outerLegArea = mainDepth * height * 2;
          const middleLegDepth = Math.max(400, mainDepth - 400); // Shorter middle leg
          const middleLegCount = Math.max(0, legCount - 2);
          const middleLegArea = middleLegDepth * height * middleLegCount;
          
          areaPerLegSqMm = (outerLegArea + middleLegArea) / legCount;
          effectiveLegCount = legCount;
          
          if (middleLegCount > 0) {
              legName = `2x Board Slab Legs (${mainDepth}mm D), ${middleLegCount}x Middle Board Legs (${middleLegDepth}mm D) x ${height}mm H`;
          } else {
              legName = `2x Board Slab Legs (${mainDepth}mm x ${height}mm)`;
          }
      } else if (legType === "box_plain") {"""

content = re.sub(
    r'      if \(legType === "board"\) \{\n          areaPerLegSqMm = mainDepth \* height;\n          effectiveLegCount = legCount;\n          legName = `\$\{legCount\}x Board Slab Legs \(\$\{mainDepth\}mm x \$\{height\}mm\)`;\n      \} else if \(legType === "box_plain"\) \{',
    replacement,
    content
)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
