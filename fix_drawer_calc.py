import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

new_drawer_calc_data = """  const drawerCalcData = useMemo(() => {
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

    const pieces: any[] = [];
    let materialCost = 0;
    let boardsSqFt = 0;

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

    // Drawer Front
    addPiece("Drawer Front", drawerWidth, drawerHeight, 1, boardThickness);
    
    // Drawer Box
    const boxThickness = 12;
    const bottomThickness = 6;
    addPiece("Drawer Sides", drawerDepth, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Back/Front", drawerWidth - 30, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Bottom", drawerWidth - 30, drawerDepth, 1, bottomThickness);

    let hardwareCost = 250; // Channels
    const hardware = [
      { label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250 }
    ];
    
    if (drawerLock) {
      hardware.push({ label: "Lock", qty: 1, cost: 120, unit: "pcs", unitPrice: 120 });
      hardwareCost += 120;
    }
    
    if (drawerHandle) {
      hardware.push({ label: "Handle", qty: 1, cost: 50, unit: "pcs", unitPrice: 50 });
      hardwareCost += 50;
    }

    const netManufacturing = materialCost + hardwareCost + 500 + 100 + 100;
    const profit = netManufacturing * 0.25;

    return {
      totals: {
        grandTotal: netManufacturing + profit,
        materialCost,
        backingCost: 0,
        boardsSqFt,
        hardwareCost,
        laborCost: 500,
        packagingCost: 100,
        toolingCost: 100,
        netManufacturingCost: netManufacturing,
        profitMargin: profit
      },
      pieces,
      hardware
    };
  }, [drawerWidth, drawerHeight, drawerDepth, drawerLock, drawerHandle, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards]);"""

content = re.sub(
    r'const drawerCalcData = \{\n    totals: \{\n      grandTotal: 3000.*?\]\n  \};',
    new_drawer_calc_data.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
