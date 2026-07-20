import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

start_str = "    const tbCost = tbSqFt * tbRate;"
end_str = "    };\n  }, [width, depth, numBays, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards]);"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

replacement = """    const tbCost = tbSqFt * tbRate;

    let totalDrawers = 0;
    let totalDoors = 0;
    bays.forEach(bay => {
       if (bay.style === '1_drawer') totalDrawers += 1;
       if (bay.style === '2_drawers') totalDrawers += 2;
       if (bay.style === '3_drawers') totalDrawers += 3;
       if (bay.style === '1_drawer_1_shutter') { totalDrawers += 1; totalDoors += 1; }
       if (bay.style === 'shutter_solid' || bay.style === 'shutter_glass') totalDoors += 1;
       if (bay.style === 'shutters_double') totalDoors += 2;
    });

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors, cost: totalDoors * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : [])
    ];
    
    const hwCost = hardware.reduce((sum, h) => sum + h.cost, 0);

    const baseMaterialCost = 4000 + tbCost + angularShelvesCost;
    const baseSqFt = 40 + tbSqFt + angularSqFt;
    const netManufacturing = baseMaterialCost + 1000 + hwCost + 3000 + 500 + 500;
    const profit = netManufacturing * 0.25;
    
    return {
      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: baseSqFt,
        materialCost: baseMaterialCost,
        backingCost: 1000,
        hardwareCost: hwCost,
        laborCost: 3000,
        packagingCost: 500,
        toolingCost: 500,
        netManufacturingCost: netManufacturing,
        profitMargin: profit
      },
      pieces: [
        { label: "Top/Bottom", l: width, w: width, h: depth, qty: 2, type: "Core", cost: tbCost, totalSqFt: tbSqFt, rate: tbRate },
        ...angularPieces
      ],
      hardware,
      bayWidth: width / (numBays || 1)
    };
  }, [width, depth, numBays, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays]);"""

content = content[:start_idx] + replacement + content[end_idx:]

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

