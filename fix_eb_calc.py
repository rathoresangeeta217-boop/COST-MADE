import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_hw = """    pieces.push(...angularPieces);

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors * 2, cost: totalDoors * 2 * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : [])
    ];"""

new_hw = """    pieces.push(...angularPieces);

    const topBottomM = 2 * (width + depth) * 2 / 1000;
    const sidePanelsM = 2 * (height + depth) * 2 / 1000;
    const partitionsM = numBays > 1 ? (numBays - 1) * 2 * (height + depth) / 1000 : 0;
    const shelvesM = totalShelves > 0 ? totalShelves * 2 * (bayWidth + depth) / 1000 : 0;
    const doorsM = totalDoors > 0 ? totalDoors * 2 * (bayWidth + height) / 1000 : 0;
    const drawersM = totalDrawers > 0 ? totalDrawers * 2 * (bayWidth + 150) / 1000 : 0;

    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(mainThk);
    const ebCost = constructionCategory === 'metal' ? 0 : totalEbMeters * ebRate;

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors * 2, cost: totalDoors * 2 * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : []),
        ...(constructionCategory !== 'metal' ? [{ label: `Edge Banding (${ebLabel})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }] : [])
    ];"""

content = content.replace(old_hw, new_hw)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
