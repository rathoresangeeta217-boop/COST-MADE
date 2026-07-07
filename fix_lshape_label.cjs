const fs = require('fs');
let file = 'src/pages/LShapeTableCalculator.tsx';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
  /\? \`All Table Modesty Panels \(/g,
  '? `All Table Modesty Panels (${modestyFinish}) ('
);
content = content.replace(
  /: \`Main Modesty Panel \(/g,
  ': `Main Modesty Panel (${modestyFinish}) ('
);

fs.writeFileSync(file, content);
console.log("Fixed labels in LShapeTableCalculator");
