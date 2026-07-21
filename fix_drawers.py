import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Fix calcData drawers
old_calc_drawers = """    if (totalDrawers > 0) {
       // approximation for drawer fronts and boxes
       addPiece("Drawer Fronts", bayWidth, 150, totalDrawers, mainThk);
       addPiece("Drawer Box Sides", depth, 100, totalDrawers * 2, 12);
       addPiece("Drawer Box Back/Front", bayWidth - 30, 100, totalDrawers * 2, 12);
       addPiece("Drawer Bottom", bayWidth - 30, depth, totalDrawers, 6);
    }"""

new_calc_drawers = """    if (totalDrawers > 0) {
       // approximation for drawer fronts and boxes
       const boxThk = constructionCategory === 'metal' ? mainThk : 12;
       const bottomThk = constructionCategory === 'metal' ? mainThk : 6;
       addPiece("Drawer Fronts", bayWidth, 150, totalDrawers, mainThk);
       addPiece("Drawer Box Sides", depth, 100, totalDrawers * 2, boxThk);
       addPiece("Drawer Box Back/Front", bayWidth - 30, 100, totalDrawers * 2, boxThk);
       addPiece("Drawer Bottom", bayWidth - 30, depth, totalDrawers, bottomThk);
    }"""

content = content.replace(old_calc_drawers, new_calc_drawers)

# Fix drawerCalcData
old_drawer_calc = """    // Drawer Box
    const boxThickness = 12;
    const bottomThickness = 6;
    addPiece("Drawer Sides", drawerDepth, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Back/Front", drawerWidth - 30, drawerHeight - 20, 2, boxThickness);
    
    addPiece("Drawer Bottom", drawerWidth - 30, drawerDepth, 1, bottomThickness);"""

new_drawer_calc = """    // Drawer Box
    const boxThickness = constructionCategory === 'metal' ? mainThk : 12;
    const bottomThickness = constructionCategory === 'metal' ? mainThk : 6;
    addPiece("Drawer Sides", drawerDepth, drawerHeight - 20, 2, boxThickness);
    addPiece("Drawer Back/Front", drawerWidth - 30, drawerHeight - 20, 2, boxThickness);
    
    addPiece("Drawer Bottom", drawerWidth - 30, drawerDepth, 1, bottomThickness);"""

content = content.replace(old_drawer_calc, new_drawer_calc)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
