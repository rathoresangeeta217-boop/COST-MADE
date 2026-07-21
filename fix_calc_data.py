import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace the beginning of calcData to define mainThk
old_start = """  const calcData = useMemo(() => {
    const getPieceRate = (label: string, defaultThickness: number) => {"""

new_start = """  const calcData = useMemo(() => {
    const mainThk = constructionCategory === 'metal' ? angleThickness : boardThickness;
    const shelfThk = constructionCategory === 'metal' ? (shelfMaterialType === 'wooden' ? woodenShelfThickness : angleThickness) : boardThickness;
    const shelfBoardId = constructionCategory === 'metal' && shelfMaterialType === 'wooden' ? woodenShelfId : boardId;
    
    const getPieceRate = (label: string, defaultThickness: number, overrideBid?: string) => {
        const key = label.replace(/\s\([^)]*(mm|Backing)\)$/, '');
        const overrideBoardId = pieceOverrides[key];
        const overrideThickness = thicknessOverrides[key];
        
        const bid = overrideBoardId && overrideBoardId !== 'default' ? overrideBoardId : (overrideBid || boardId);
        const thk = overrideThickness || defaultThickness;
        const b = boards.find(b => b.id === bid) || getBoards(quality, 'wooden').find(b => b.id === bid);
        if (!b) return 100;
        return getBoardRate(bid, b.costPerSqFt, thk, quality);
    };"""

content = content.replace(old_start, new_start)

# Now we need to change how rate is calculated in angularPieces
old_angular = """    const angularPieces = angularShelves.map((s, i) => {
        const label = `Angular Shelf ${i+1}`;
        const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
        const area = (length * depth) / 90000;
        const rate = getPieceRate(label, boardThickness);
        const cost = area * rate;
        angularSqFt += area;
        angularShelvesCost += cost;
        return { label, l: length, w: length, h: depth, qty: 1, type: "Core", cost, totalSqFt: area, rate };
    });"""

new_angular = """    const angularPieces = angularShelves.map((s, i) => {
        const label = `Angular Shelf ${i+1}`;
        const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
        const area = (length * depth) / 90000;
        const rate = getPieceRate(label, shelfThk, shelfBoardId);
        const cost = area * rate;
        angularSqFt += area;
        angularShelvesCost += cost;
        return { label, l: length, w: length, h: shelfThk, qty: 1, type: "Core", cost, totalSqFt: area, rate };
    });"""

content = content.replace(old_angular, new_angular)

# Replace addPiece to take an optional overrideBid
old_add_piece = """    const addPiece = (label: string, l: number, w: number, qty: number, defaultThk: number) => {
      const area = (l * w) / 90000;
      const totalArea = area * qty;
      const rate = getPieceRate(label, defaultThk);
      const cost = totalArea * rate;
      pieces.push({ label, l, w, h: defaultThk, qty, type: "Core", cost, totalSqFt: totalArea, rate });
      materialCost += cost;
      boardsSqFt += totalArea;
      return cost;
    };"""

new_add_piece = """    const addPiece = (label: string, l: number, w: number, qty: number, defaultThk: number, overrideBid?: string) => {
      const area = (l * w) / 90000;
      const totalArea = area * qty;
      const rate = getPieceRate(label, defaultThk, overrideBid);
      const cost = totalArea * rate;
      pieces.push({ label, l, w, h: defaultThk, qty, type: "Core", cost, totalSqFt: totalArea, rate });
      materialCost += cost;
      boardsSqFt += totalArea;
      return cost;
    };"""

content = content.replace(old_add_piece, new_add_piece)

# Replace the hardcoded boardThickness in addPiece calls
old_main = """    // Main carcass
    addPiece("Top/Bottom", width, depth, 2, boardThickness);
    addPiece("Side Panels", height, depth, 2, boardThickness);
    if (numBays > 1) {
      addPiece("Vertical Partitions", height, depth, numBays - 1, boardThickness);
    }"""

new_main = """    // Main carcass
    addPiece("Top/Bottom", width, depth, 2, mainThk);
    addPiece("Side Panels", height, depth, 2, mainThk);
    if (numBays > 1) {
      addPiece("Vertical Partitions", height, depth, numBays - 1, mainThk);
    }"""

content = content.replace(old_main, new_main)

old_shelves = """    if (totalShelves > 0) {
       addPiece("Horizontal Shelves", bayWidth, depth, totalShelves, boardThickness);
    }
    
    if (totalDoors > 0) {
       addPiece("Shutters / Doors", bayWidth, height, totalDoors, boardThickness);
    }
    
    if (totalDrawers > 0) {
       // approximation for drawer fronts and boxes
       addPiece("Drawer Fronts", bayWidth, 150, totalDrawers, boardThickness);"""

new_shelves = """    if (totalShelves > 0) {
       addPiece("Horizontal Shelves", bayWidth, depth, totalShelves, shelfThk, shelfBoardId);
    }
    
    if (totalDoors > 0) {
       addPiece("Shutters / Doors", bayWidth, height, totalDoors, mainThk);
    }
    
    if (totalDrawers > 0) {
       // approximation for drawer fronts and boxes
       addPiece("Drawer Fronts", bayWidth, 150, totalDrawers, mainThk);"""

content = content.replace(old_shelves, new_shelves)

# Fix Edge banding logic - use mainThk instead of boardThickness
old_eb = """    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(boardThickness);
    const ebCost = totalEbMeters * ebRate;"""

new_eb = """    let totalEbMeters = (topBottomM + sidePanelsM + partitionsM + shelvesM + doorsM + drawersM) * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(mainThk);
    const ebCost = constructionCategory === 'metal' ? 0 : totalEbMeters * ebRate;"""

content = content.replace(old_eb, new_eb)

old_eb_label = """        { label: `Edge Banding (${ebLabel})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }"""
new_eb_label = """        ...(constructionCategory !== 'metal' ? [{ label: `Edge Banding (${ebLabel})`, qty: Number(totalEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }] : [])"""
content = content.replace(old_eb_label, new_eb_label)

# Dependencies update
old_deps = "  }, [width, height, depth, numBays, numRows, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays]);"
new_deps = "  }, [width, height, depth, numBays, numRows, angularShelves, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, bays, constructionCategory, angleThickness, shelfMaterialType, woodenShelfId, woodenShelfThickness]);"
content = content.replace(old_deps, new_deps)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
