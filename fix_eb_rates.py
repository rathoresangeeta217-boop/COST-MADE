import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# Add getEdgeBandingRate
eb_func = """
export const getEdgeBandingRate = (thickness: number) => {
  if (thickness <= 18) return { rate: 13, label: "0.8mm" };
  if (thickness <= 25) return { rate: 28, label: "2mm" };
  return { rate: 48, label: "40mm" };
};
"""

if "getEdgeBandingRate" not in content:
    content = content.replace('export const getBoards = (quality: string) => [', eb_func + '\nexport const getBoards = (quality: string) => [')

# Update Table Top Edge banding
top_eb = """    let edgeBandingRate = 13;
    let edgeBandingThickness = "0.8mm";
    if (topThickness === 25) {
      edgeBandingRate = 28;
      edgeBandingThickness = "2mm";
    } else if (topThickness === 36) {
      edgeBandingRate = 48;
      edgeBandingThickness = "0.40mm"; // User mentioned .40 mm
    }"""
new_top_eb = """    const { rate: edgeBandingRate, label: edgeBandingThickness } = getEdgeBandingRate(topThickness);"""
content = content.replace(top_eb, new_top_eb)

# Update Legs Edge banding
leg_eb = """    const legEdgeBandingCost = legPerimeterM * 13;
    bCostTotal += legEdgeBandingCost;
    bDetails.push({
      label: `Legs Edge Banding (0.8mm, ${legPerimeterM.toFixed(3)}m)`,
      cost: Math.round(legEdgeBandingCost),
    });"""
new_leg_eb = """    const { rate: legEbRate, label: legEbLabel } = getEdgeBandingRate(18); // assuming legs are 18mm board
    const legEdgeBandingCost = legPerimeterM * legEbRate;
    bCostTotal += legEdgeBandingCost;
    bDetails.push({
      label: `Legs Edge Banding (${legEbLabel}, ${legPerimeterM.toFixed(3)}m)`,
      cost: Math.round(legEdgeBandingCost),
    });"""
content = content.replace(leg_eb, new_leg_eb)

# Update Modesty Edge banding
mod_eb = """      const modestyEbLengthM = (modestyWidth / 1000) * 1.2 * actualPersons;
      const modestyEbCost = modestyEbLengthM * 13; 
      bCostTotal += modestyEbCost;
      bDetails.push({
        label: `Modesty Edge Banding (0.8mm, ${modestyEbLengthM.toFixed(3)}m)`,
        cost: Math.round(modestyEbCost),
      });"""
new_mod_eb = """      const modestyEbLengthM = (modestyWidth / 1000) * 1.2 * actualPersons;
      const { rate: modEbRate, label: modEbLabel } = getEdgeBandingRate(18); // assuming modesty is 18mm
      const modestyEbCost = modestyEbLengthM * modEbRate; 
      bCostTotal += modestyEbCost;
      bDetails.push({
        label: `Modesty Edge Banding (${modEbLabel}, ${modestyEbLengthM.toFixed(3)}m)`,
        cost: Math.round(modestyEbCost),
      });"""
content = content.replace(mod_eb, new_mod_eb)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
