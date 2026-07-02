const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const regex1DrawerOpen = /\{\/\* Render open adjustable shelves inside remaining space below drawer \(segmented & draggable\) \*\/\}.*?return elements;\s*\}\)\(\)\}/s;
content = content.replace(regex1DrawerOpen, `{/* Render open adjustable shelves inside remaining space below drawer (segmented & draggable) */}
                                      {renderShelves(bay, idx, bayX, dY + dH - 2, bayW, bayH - dH)}`);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched 1_drawer_open shelves");
