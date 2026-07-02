const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
const oldOpenSvgRegex = /\{\/\* Draw horizontal open shelves \(segmented\) \*\/\}.*?return elements;\s*\}\)\(\)\}/s;
console.log(oldOpenSvgRegex.test(content));
