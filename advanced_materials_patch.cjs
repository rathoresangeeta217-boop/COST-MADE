const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// 1. Add State
content = content.replace(
  /const \[boardThickness, setBoardThickness\] = useState<number>\(18\);/,
  `const [boardThickness, setBoardThickness] = useState<number>(18);
  const [shutterBoardId, setShutterBoardId] = useState<string>("default");
  const [backPanelBoardId, setBackPanelBoardId] = useState<string>("default");
  const [drawerBoxBoardId, setDrawerBoxBoardId] = useState<string>("default");`
);

// 2. Add to loader
content = content.replace(
  /if \(c\.boardThickness !== undefined\) setBoardThickness\(c\.boardThickness\);/,
  `if (c.boardThickness !== undefined) setBoardThickness(c.boardThickness);
        if (c.shutterBoardId !== undefined) setShutterBoardId(c.shutterBoardId);
        if (c.backPanelBoardId !== undefined) setBackPanelBoardId(c.backPanelBoardId);
        if (c.drawerBoxBoardId !== undefined) setDrawerBoxBoardId(c.drawerBoxBoardId);`
);

// 3. Add to itemData
content = content.replace(
  /bays\n\s*\},/,
  `bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId\n                  },`
);

// 4. Modify calcData dependencies
content = content.replace(
  /numBays, bays, rateToUse, supportLegsCount\]\);/,
  `numBays, bays, rateToUse, supportLegsCount, shutterBoardId, backPanelBoardId, drawerBoxBoardId]);`
);
content = content.replace(
  /drawerLock, drawerHandle, rateToUse\]\);/,
  `drawerLock, drawerHandle, rateToUse, drawerBoxBoardId, shutterBoardId]);`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched states");
