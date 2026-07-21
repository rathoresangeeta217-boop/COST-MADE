import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

eb_func = """
export const getEdgeBandingRate = (thickness: number) => {
  if (thickness <= 18) return { rate: 13, label: "0.8mm" };
  if (thickness <= 25) return { rate: 28, label: "2mm" };
  return { rate: 48, label: "40mm" };
};
"""

if "getEdgeBandingRate" not in content:
    content = content.replace('export const getBoards = (quality: string, category: string = "wooden") => {', eb_func + '\nexport const getBoards = (quality: string, category: string = "wooden") => {')

# Find EB usage in CustomStorageCalculator and replace with getEdgeBandingRate
# We added this earlier: const ebRate = boardThickness > 18 ? 28 : 13;
old_eb = """    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    // Base rate for 0.8mm edge banding is 13 Rs/m. 
    // If board is thicker, say 25mm, we might use 28 Rs/m.
    const ebRate = boardThickness > 18 ? 28 : 13;
    const ebCost = totalEbMeters * ebRate;"""
new_eb = """    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(boardThickness);
    const ebCost = totalEbMeters * ebRate;"""
content = content.replace(old_eb, new_eb)

old_eb_label = """{ label: `Edge Banding (${boardThickness > 18 ? "2mm" : "0.8mm"})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }"""
new_eb_label = """{ label: `Edge Banding (${ebLabel})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }"""
content = content.replace(old_eb_label, new_eb_label)

old_drawer_eb = """    const drawerEbMeters = (2 * (drawerWidth + drawerHeight)) / 1000 * 1.2;
    const ebRate = boardThickness > 18 ? 28 : 13;
    const ebCost = drawerEbMeters * ebRate;"""
new_drawer_eb = """    const drawerEbMeters = (2 * (drawerWidth + drawerHeight)) / 1000 * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(boardThickness);
    const ebCost = drawerEbMeters * ebRate;"""
content = content.replace(old_drawer_eb, new_drawer_eb)

old_drawer_eb_label = """{ label: `Edge Banding (${boardThickness > 18 ? "2mm" : "0.8mm"})`, qty: Number(drawerEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }"""
new_drawer_eb_label = """{ label: `Edge Banding (${ebLabel})`, qty: Number(drawerEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }"""
content = content.replace(old_drawer_eb_label, new_drawer_eb_label)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
