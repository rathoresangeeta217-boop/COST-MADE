import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """      if (legType === "board") {
          areaPerLegSqMm = mainDepth * height;
          effectiveLegCount = legCount;
          legName = `${legCount}x Board Slab Legs (${mainDepth}mm x ${height}mm)`;
      } else if (legType === "box_plain") {"""

content = re.sub(
    r'      if \(legType === "board"\) \{\n          areaPerLegSqMm = mainDepth \* height;\n          effectiveLegCount = 2;\n          legName = `2x Board Slab Legs \(\$\{mainDepth\}mm x \$\{height\}mm\)`;\n      \} else if \(legType === "box_plain"\) \{',
    replacement,
    content
)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
