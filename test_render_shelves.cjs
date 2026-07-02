const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
console.log(content.includes('renderShelves'));
