import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate

      if (legType === "board") {
          areaPerLegSqMm = (mainDepth - 200) * height; // simple slab
          legDesc = `${legCount}x Board Slab Legs`;
      } else if (legType === "box_plain") {
          areaPerLegSqMm = (400 * 4) * height; // 400x400 box
          legDesc = `${legCount}x Box Legs (Plain)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (400 * 4) * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Box Legs (Fluted)`;
      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legDesc = `${legCount}x Round Legs (Plain)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Round Legs (Fluted)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * legCount) / 90000;"""

new_block = """  } else {
      let areaPerLegSqMm = 0;
      let legRate = board.costPerSqFt; // use base rate
      let currentLegCount = legCount;

      if (legType === "board") {
          areaPerLegSqMm = mainDepth * height;
          currentLegCount = 2;
          legDesc = `2x Board Slab Legs`;
      } else if (legType === "box_plain") {
          areaPerLegSqMm = (400 * 4) * height; // 400x400 box
          legDesc = `${legCount}x Box Legs (Plain)`;
      } else if (legType === "box_fluted") {
          areaPerLegSqMm = (400 * 4) * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Box Legs (Fluted)`;
      } else if (legType === "round_plain") {
          areaPerLegSqMm = 1200 * height; // ~380 dia
          legDesc = `${legCount}x Round Legs (Plain)`;
      } else if (legType === "round_fluted") {
          areaPerLegSqMm = 1200 * height;
          legRate += 100; // fluted premium
          legDesc = `${legCount}x Round Legs (Fluted)`;
      }

      const totalLegAreaSqFt = (areaPerLegSqMm * currentLegCount) / 90000;"""

content = content.replace(old_block, new_block)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
