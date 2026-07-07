import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legName = `${legCount}x Round Legs (Plain) (~380mm dia x ${height}mm)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Round Legs (Fluted) (~380mm dia x ${height}mm)`;
      }"""

new_block = """      } else if (legType === "round_plain") {
          const circumference = Math.round(Math.PI * 600); // 1885mm for 600mm dia
          areaPerLegSqMm = circumference * height;
          legName = `${legCount}x Round Legs (Plain) (600mm dia x ${height}mm)`;
      } else if (legType === "round_fluted") {
          const circumference = Math.round(Math.PI * 600); // 1885mm for 600mm dia
          areaPerLegSqMm = circumference * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Round Legs (Fluted) (600mm dia x ${height}mm)`;
      }"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
