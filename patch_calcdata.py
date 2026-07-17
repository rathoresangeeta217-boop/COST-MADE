import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """  const calcData = {
    totals: {
      grandTotal: 15000,
      boardsSqFt: 50,
      materialCost: 5000,
      backingCost: 1000,
      hardwareCost: 2000,
      laborCost: 3000,
      packagingCost: 500,
      toolingCost: 500,
      netManufacturingCost: 12000,
      profitMargin: 3000
    },
    pieces: [
      { label: "Top/Bottom", l: width, w: width, h: depth, qty: 2, type: "Core", cost: 1000, totalSqFt: 10, rate: 100 }
    ],
    hardware: [
      { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 }
    ],
    bayWidth: width / (numBays || 1)
  };"""

replacement = """  const calcData = useMemo(() => {
    let angularShelvesCost = 0;
    let angularSqFt = 0;
    const rate = 100; // Mock rate
    const angularPieces = angularShelves.map((s, i) => {
        const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
        const area = (length * depth) / 90000;
        const cost = area * rate;
        angularSqFt += area;
        angularShelvesCost += cost;
        return { label: `Angular Shelf ${i+1}`, l: length, w: length, h: depth, qty: 1, type: "Core", cost, totalSqFt: area, rate };
    });

    const baseMaterialCost = 5000 + angularShelvesCost;
    const baseSqFt = 50 + angularSqFt;
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
        { label: "Top/Bottom", l: width, w: width, h: depth, qty: 2, type: "Core", cost: 1000, totalSqFt: 10, rate: 100 },
        ...angularPieces
      ],
      hardware: [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 }
      ],
      bayWidth: width / (numBays || 1)
    };
  }, [width, depth, numBays, angularShelves]);"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
