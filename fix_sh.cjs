const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

content = content.replace(/\.\.\.getCustomMat\('shutter', rateToUse\),\s*customCostPerSqFt: sh\.cost,/g,
  "customCostPerSqFt: getCustomMat('shutter', rateToUse).cost,");

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Fixed sh.cost");
