import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

eb_drawer_calc_str = """
    addPiece("Drawer Bottom", drawerWidth - 30, drawerDepth, 1, bottomThickness);

    const drawerEbMeters = (2 * (drawerWidth + drawerHeight)) / 1000 * 1.2;
    const ebRate = boardThickness > 18 ? 28 : 13;
    const ebCost = drawerEbMeters * ebRate;

    let hardwareCost = 250 + ebCost; // Channels + EB
    const hardware = [
      { label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250 },
      { label: `Edge Banding (${boardThickness > 18 ? "2mm" : "0.8mm"})`, qty: Number(drawerEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }
    ];
"""

content = re.sub(
    r'addPiece\("Drawer Bottom", drawerWidth - 30, drawerDepth, 1, bottomThickness\);\s*let hardwareCost = 250; // Channels\s*const hardware = \[\s*\{\s*label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250\s*\}\s*\];',
    eb_drawer_calc_str.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
