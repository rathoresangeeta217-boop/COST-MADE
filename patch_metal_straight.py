import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_metal = """  if (legType === "metal_straight") {
      legCostTotal = legCount * 1500;
      legDesc = `${legCount}x Metal Straight Legs`;
  } else if (legType === "metal_u") {"""

new_metal = """  let hardwareLegCost = 0;
  let hardwareLegDesc = "";

  if (legType === "metal_straight" || legType === "metal_u") {
      // Calculate like normal table (pipe dimensions)
      let verticalLengthMm = legCount * 2 * height;
      if (legType === "metal_u") {
          verticalLengthMm += legCount * mainDepth; // u-shape has bottom loops
      }
      const verticalFeet = verticalLengthMm / 304.8;
      const verticalRate = 27; // 40x40 pipe
      const costVerticals = verticalFeet * verticalRate;

      // 40x20 Pipe for horizontal supports
      const horizontalWidthMm = 2 * Math.max(0, mainWidth - 140);
      const horizontalDepthMm = Math.max(0, mainDepth - 180) * legCount;
      const horizontalLengthMm = horizontalWidthMm + horizontalDepthMm;
      const horizontalFeet = horizontalLengthMm / 304.8;
      const cost40x20 = horizontalFeet * 19.6;

      const totalFeet = verticalFeet + horizontalFeet;
      const powderCoatingCost = totalFeet * 30;

      const numLegs = legCount * 2;
      const bufferCost = numLegs * 7;
      const nutCost = numLegs * 5;
      const butterflyCost = numLegs * 2 * 12.5;
      const accessoriesCost = bufferCost + nutCost + butterflyCost;

      hardwareLegCost = costVerticals + cost40x20 + powderCoatingCost + accessoriesCost;
      hardwareLegDesc = legType === "metal_straight" ? `Metal Straight Legs Framework` : `Metal U-Shape Legs Framework`;
  } else {"""

content = content.replace(old_metal, new_metal)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
