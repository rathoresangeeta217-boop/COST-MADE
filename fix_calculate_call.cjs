const fs = require('fs');
let file = 'src/pages/LShapeTableCalculator.tsx';
let content = fs.readFileSync(file, 'utf8');

// Fix 1: Add modestyFinish to useMemo dependencies and calculateLShapeCost arguments
content = content.replace(
  /modestyType,\n\s*metalModestyType,/g,
  `modestyType,\n      modestyFinish,\n      metalModestyType,`
);

// Fix 2: Add modestyFinish: "plain" to the two export calls
content = content.replace(
  /modestyType: exportModestyType,\n\s*metalModestyType: "plain",/g,
  `modestyType: exportModestyType,\n                modestyFinish: "plain",\n                metalModestyType: "plain",`
);

fs.writeFileSync(file, content);
console.log("Fixed calculate calls in LShapeTableCalculator");
