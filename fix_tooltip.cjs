const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

content = content.replace(
  /Interactive Mode: Click on doors to open\/close them. Click on internal shelf lines to remove\/restore them./,
  `Interactive Mode: Click doors to open/close. Click shelf lines to remove/restore. Drag shelves to adjust positions.`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated tooltip");
