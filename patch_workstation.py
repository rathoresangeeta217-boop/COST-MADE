import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Add isHeightAdjustable to calculateWorkstationCost signature
old_sig = """  layout = "linear",
}: any) {"""
new_sig = """  layout = "linear",
  isHeightAdjustable = false,
}: any) {"""
content = content.replace(old_sig, new_sig)

# 2. Modify legs / understructure calculation
old_legs = """  // 2. Legs / Understructure
  let hCost = 0;
  const hDetails: {
    label: string;
    cost: number;
    qty: number;
    unitPrice: number;
    unitLabel: string;
  }[] = [];

  const legFrames = legCountOverride && legCountOverride > 0 ? legCountOverride : cols + 1; // Number of vertical supports
  const clusterDepth = depth * rows;

  if (legId === "board") {"""

new_legs = """  // 2. Legs / Understructure
  let hCost = 0;
  const hDetails: {
    label: string;
    cost: number;
    qty: number;
    unitPrice: number;
    unitLabel: string;
  }[] = [];

  const legFrames = legCountOverride && legCountOverride > 0 ? legCountOverride : cols + 1; // Number of vertical supports
  const clusterDepth = depth * rows;

  if (layout === "linear" && isHeightAdjustable) {
    const frameCost = width <= 1200 ? 9500 : 13500;
    const totalHACost = frameCost * numPersons;
    hCost += totalHACost;
    hDetails.push({
      label: `Height Adjustment Frame (${width}mm W)`,
      qty: numPersons,
      unitPrice: frameCost,
      unitLabel: "pcs",
      cost: totalHACost,
    });
  } else if (legId === "board") {"""
content = content.replace(old_legs, new_legs)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
