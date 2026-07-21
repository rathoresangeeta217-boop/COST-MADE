import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

eb_calc_str = """
    pieces.push(...angularPieces);

    // Edge Banding approximation (in meters, including 20% wastage)
    const topBottomM = (2 * width) / 1000;
    const sidePanelsM = (2 * height) / 1000;
    const partitionsM = ((numBays - 1) * height) / 1000;
    const shelvesM = (totalShelves * bayWidth) / 1000;
    const doorsM = (totalDoors * 2 * (bayWidth + height)) / 1000;
    const drawersM = (totalDrawers * 2 * (bayWidth + 150)) / 1000;
    
    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    // Base rate for 0.8mm edge banding is 13 Rs/m. 
    // If board is thicker, say 25mm, we might use 28 Rs/m.
    const ebRate = boardThickness > 18 ? 28 : 13;
    const ebCost = totalEbMeters * ebRate;

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors * 2, cost: totalDoors * 2 * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : []),
        { label: `Edge Banding (${boardThickness > 18 ? "2mm" : "0.8mm"})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }
    ];
"""

content = re.sub(
    r'pieces\.push\(\.\.\.angularPieces\);\s*const hardware = \[\s*\{ label: "Screws"[^\]]*\];',
    eb_calc_str.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
