import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      let effectiveLegCount = legCount;
      let legName = "";

      if (legType === "board") {
          areaPerLegSqMm = mainDepth * height;
          effectiveLegCount = 2;
          legName = `2x Board Slab Legs (${mainDepth}mm x ${height}mm)`;
      } else if (legType === "box_plain") {
          areaPerLegSqMm = (600 * 4) * height; // 600x600 box
          legName = `${legCount}x Box Legs (Plain) (600mm x 600mm x ${height}mm)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (600 * 4) * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Box Legs (Fluted) (600mm x 600mm x ${height}mm)`;
      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legName = `${legCount}x Round Legs (Plain) (~380mm dia x ${height}mm)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Round Legs (Fluted) (~380mm dia x ${height}mm)`;
      }"""

new_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      let effectiveLegCount = legCount;
      let legName = "";

      if (legType === "board") {
          areaPerLegSqMm = mainDepth * height;
          effectiveLegCount = 2;
          legName = `2x Board Slab Legs (${mainDepth}mm x ${height}mm)`;
      } else if (legType === "box_plain") {
          areaPerLegSqMm = (600 * 4) * height; // 600x600 box
          legName = `${legCount}x Box Legs (Plain) (4 panels of 600mm x ${height}mm)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (600 * 4) * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Box Legs (Fluted) (4 panels of 600mm x ${height}mm)`;
      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legName = `${legCount}x Round Legs (Plain) (~380mm dia x ${height}mm)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legName = `${legCount}x Round Legs (Fluted) (~380mm dia x ${height}mm)`;
      }"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
