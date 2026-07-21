import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Fix getPieceRate in drawerCalcData
old_drawer_get = """    const drawerCalcData = useMemo(() => {
    const getPieceRate = (label: string, defaultThickness: number) => {
        const key = label.replace(/\s\([^)]*(mm|Backing)\)$/, '');
        const overrideBoardId = pieceOverrides[key];
        const overrideThickness = thicknessOverrides[key];
        
        const bid = overrideBoardId && overrideBoardId !== 'default' ? overrideBoardId : boardId;
        const thk = overrideThickness || defaultThickness;
        const b = boards.find(b => b.id === bid);
        if (!b) return 100;
        return getBoardRate(bid, b.costPerSqFt, thk, quality);
    };"""

new_drawer_get = """    const drawerCalcData = useMemo(() => {
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

content = content.replace(old_drawer_get, new_drawer_get)

# Also fix drawerCalcData to use mainThk and add dependencies
old_drawer_body = """    // Drawer Front
    addPiece("Drawer Front", drawerWidth, drawerHeight, 1, boardThickness);
    
    // Drawer Box
    const boxThickness = 12;
    const bottomThickness = 6;
    addPiece("Drawer Sides", drawerDepth, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Back/Front", drawerWidth - 30, drawerHeight - 20, 2, boxThickness);"""

new_drawer_body = """    // Drawer Front
    const mainThk = constructionCategory === 'metal' ? angleThickness : boardThickness;
    addPiece("Drawer Front", drawerWidth, drawerHeight, 1, mainThk);
    
    // Drawer Box
    const boxThickness = 12;
    const bottomThickness = 6;
    addPiece("Drawer Sides", drawerDepth, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Back/Front", drawerWidth - 30, drawerHeight - 20, 2, boxThickness);"""

content = content.replace(old_drawer_body, new_drawer_body)

# Edge banding logic in drawer
old_drawer_eb = """    const drawerEbMeters = (2 * (drawerWidth + drawerHeight)) / 1000 * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(boardThickness);
    const ebCost = drawerEbMeters * ebRate;

    let hardwareCost = 250 + ebCost; // Channels + EB
    const hardware = [
      { label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250 },
      { label: `Edge Banding (${ebLabel})`, qty: Number(drawerEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }
    ];"""

new_drawer_eb = """    const drawerEbMeters = (2 * (drawerWidth + drawerHeight)) / 1000 * 1.2;
    const { rate: ebRate, label: ebLabel } = getEdgeBandingRate(mainThk);
    const ebCost = constructionCategory === 'metal' ? 0 : drawerEbMeters * ebRate;

    let hardwareCost = 250 + ebCost; // Channels + EB
    const hardware = [
      { label: "Channels", qty: 1, cost: 250, unit: "pair", unitPrice: 250 },
      ...(constructionCategory !== 'metal' ? [{ label: `Edge Banding (${ebLabel})`, qty: Number(drawerEbMeters.toFixed(2)), cost: ebCost, unit: "m", unitPrice: ebRate }] : [])
    ];"""

content = content.replace(old_drawer_eb, new_drawer_eb)

old_drawer_deps = """  }, [drawerWidth, drawerHeight, drawerDepth, drawerLock, drawerHandle, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards]);"""
new_drawer_deps = """  }, [drawerWidth, drawerHeight, drawerDepth, drawerLock, drawerHandle, pieceOverrides, thicknessOverrides, boardId, boardThickness, quality, boards, constructionCategory, angleThickness]);"""
content = content.replace(old_drawer_deps, new_drawer_deps)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
