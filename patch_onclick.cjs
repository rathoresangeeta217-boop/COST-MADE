const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

content = content.replace(/onClick=\{\(e\) \=\> e\.stopPropagation\(\)\}/g, 'onClick={(e) => { e.stopPropagation(); togglePartition(pId, idx); }}');

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched onClick to call togglePartition");
