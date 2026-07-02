const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
const old1DrawerOpenSvgRegex = /\{\/\* Render open adjustable shelves inside remaining space below drawer \(segmented\) \*\/\}.*?return elements;\s*\}\)\(\)\}/s;
console.log(old1DrawerOpenSvgRegex.test(content));
