import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Let's write the new body of calcData.

new_calc_data = """  const calcData = useMemo(() => {
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

    const pieces: any[] = [];
    let materialCost = angularShelvesCost;
    let boardsSqFt = angularSqFt;

    const addPiece = (label: string, l: number, w: number, qty: number, defaultThk: number) => {
      const area = (l * w) / 90000;
      const totalArea = area * qty;
      const rate = getPieceRate(label, defaultThk);
      const cost = totalArea * rate;
      pieces.push({ label, l, w, h: defaultThk, qty, type: "Core", cost, totalSqFt: totalArea, rate });
      materialCost += cost;
      boardsSqFt += totalArea;
      return cost;
    };

    // Main carcass
    addPiece("Top/Bottom", width, depth, 2, boardThickness);
    addPiece("Side Panels", height, depth, 2, boardThickness);
    if (numBays > 1) {
      addPiece("Vertical Partitions", height, depth, numBays - 1, boardThickness);
    }
    
    // Back Panel
    const backPanelThk = 6; // default back panel thickness
    addPiece("Back Panel", width, height, 1, backPanelThk);

    // Bays internals
    let totalDrawers = 0;
    let totalDoors = 0;
    let totalShelves = 0;
    
    const bayWidth = width / (numBays || 1);
    
    bays.forEach(bay => {
       if (bay.style === '1_drawer') totalDrawers += 1;
       if (bay.style === '2_drawers') totalDrawers += 2;
       if (bay.style === '3_drawers') totalDrawers += 3;
       if (bay.style === '1_drawer_1_shutter') { totalDrawers += 1; totalDoors += 1; }
       if (bay.style === 'shutter_solid' || bay.style === 'shutter_glass') totalDoors += 1;
       if (bay.style === 'shutters_double') totalDoors += 2;
       totalShelves += (bay.shelves || 0);
    });
    
    if (totalShelves > 0) {
       addPiece("Horizontal Shelves", bayWidth, depth, totalShelves, boardThickness);
    }
    
    if (totalDoors > 0) {
       addPiece("Shutters / Doors", bayWidth, height, totalDoors, boardThickness);
    }
    
    if (totalDrawers > 0) {
       // approximation for drawer fronts and boxes
       addPiece("Drawer Fronts", bayWidth, 150, totalDrawers, boardThickness);
       addPiece("Drawer Box Sides", depth, 100, totalDrawers * 2, 12);
       addPiece("Drawer Box Back/Front", bayWidth - 30, 100, totalDrawers * 2, 12);
       addPiece("Drawer Bottom", bayWidth - 30, depth, totalDrawers, 6);
    }
    
    pieces.push(...angularPieces);

    const hardware = [
        { label: "Screws", qty: 50, cost: 200, unit: "pcs", unitPrice: 4 },
        ...(totalDoors > 0 ? [{ label: "Hinges", qty: totalDoors * 2, cost: totalDoors * 2 * 150, unit: "pair", unitPrice: 150 }] : []),
        ...(totalDrawers > 0 ? [{ label: "Channels", qty: totalDrawers, cost: totalDrawers * 250, unit: "pair", unitPrice: 250 }] : [])
    ];
    
    const hwCost = hardware.reduce((sum, h) => sum + h.cost, 0);

    const netManufacturing = materialCost + hwCost + 3000 + 500 + 500;
    const profit = netManufacturing * 0.25;
    
    return {
      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: boardsSqFt,
        materialCost: materialCost,
        backingCost: 0,
        hardwareCost: hwCost,
        laborCost: 3000,
        packagingCost: 500,
        toolingCost: 500,
        netManufacturingCost: netManufacturing,
        profitMargin: profit
      },
      pieces,
      hardware,
      bayWidth
    };
  }, [width, height, depth, numBays, numRows, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays]);"""

content = re.sub(
    r'const calcData = useMemo\(\(\) => \{.*?\n  \}, \[width, depth, numBays, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays\]\);',
    new_calc_data.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
