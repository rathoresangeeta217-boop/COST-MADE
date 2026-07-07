import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# Update signature
old_sig = """  wireManagement,
  addLeatherlite,
  legCountInput,
}: any) {"""
new_sig = """  wireManagement,
  addLeatherlite,
  legCountInput,
  includeModesty,
  modestyType,
  customModestyHeight,
  modestyFinish,
}: any) {"""

content = content.replace(old_sig, new_sig)

# Add Modesty Calculation after Add-ons or Board pieces
modesty_logic = """
  // Modesty Calculation
  if (includeModesty) {
      let modestyHeightMm = 450;
      if (modestyType === "standard") modestyHeightMm = 715;
      else if (modestyType === "short") modestyHeightMm = 600;
      else if (modestyType === "shorter") modestyHeightMm = 300;
      else if (modestyType === "custom") modestyHeightMm = customModestyHeight || 300;

      const modestyAreaSqMm = mainWidth * modestyHeightMm;
      let modestyRate = board.costPerSqFt;
      if (modestyFinish === "fluted") modestyRate += 100;
      
      const modestyAreaSqFt = modestyAreaSqMm / 90000;
      const modestyCost = modestyAreaSqFt * modestyRate;

      bDetails.push({
          label: `Modesty Panel (${modestyFinish}) - ${mainWidth}x${modestyHeightMm}mm (${modestyAreaSqFt.toFixed(2)} sq.ft)`,
          cost: Math.round(modestyCost),
      });
      bCostTotal += modestyCost;
  }
"""

# Find where bCostTotal is updated for legs, maybe we just put it right before hardware/addons or after top calculation
content = content.replace("  // Legs Calculation", modesty_logic + "\n  // Legs Calculation")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
