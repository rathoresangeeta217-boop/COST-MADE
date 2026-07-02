const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const regexOpen = /\{\/\* Draw horizontal and vertical open shelves \(segmented & draggable\) \*\/\}.*?return elements;\s*\}\)\(\)\}/s;
content = content.replace(regexOpen, `{/* Draw horizontal and vertical open shelves (segmented & draggable) */}
                                {renderShelves(bay, idx, bayX, bayY, bayW, bayH)}`);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched open shelves");
