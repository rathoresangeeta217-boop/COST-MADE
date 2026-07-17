import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

start_str = "  const calcData = useMemo(() => {"
end_str = "  }, [width, depth, numBays, angularShelves]);"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

replacement = """  const calcData = useMemo(() => {
    const getPieceRate = (label: string, defaultThickness: number) => {
        const key = label.replace(/\s\([^)]*(mm|Backing)\)$/, '');
        const overrideBoardId = pieceOverrides[key];
        const overrideThickness = thicknessOverrides[key];
        
        const bid = overrideBoardId && overrideBoardId !== 'default' ? overrideBoardId : boardId;
        const thk = overrideThickness || defaultThickness;
        const b = boards.find(b => b.id === bid);
        if (!b) return 100;
        return getBoardRate(bid, b.costPerSqFt, thk, quality);
    };

    let angularShelvesCost = 0;
    let angularSqFt = 0;
    
    const angularPieces = angularShelves.map((s, i) => {
        const label = `Angular Shelf ${i+1}`;
        const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
        const area = (length * depth) / 90000;
        const rate = getPieceRate(label, boardThickness);
        const cost = area * rate;
        angularSqFt += area;
        angularShelvesCost += cost;
        return { label, l: length, w: length, h: depth, qty: 1, type: "Core", cost, totalSqFt: area, rate };
    });

    const tbSqFt = 10;
    const tbRate = getPieceRate("Top/Bottom", boardThickness);
    const tbCost = tbSqFt * tbRate;

    const baseMaterialCost = 4000 + tbCost + angularShelvesCost;
    const baseSqFt = 40 + tbSqFt + angularSqFt;
    const netManufacturing = baseMaterialCost + 1000 + 2000 + 3000 + 500 + 500;
    const profit = netManufacturing * 0.25;
    
    return {
      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: baseSqFt,
        materialCost: baseMaterialCost,
        backingCost: 1000,
        hardwareCost: 2000,
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
      hardware: [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 }
      ],
      bayWidth: width / (numBays || 1)
    };
  }, [width, depth, numBays, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards]);"""

content = content[:start_idx] + replacement + content[end_idx:]

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
