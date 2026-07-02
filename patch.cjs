const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

content = content.replace(/className=\{isFullScreenDrawing \? "cursor-pointer hover:opacity-80 transition-opacity" : ""\} onClick=\{\(\) => isFullScreenDrawing && toggleDoor/g, 'className="cursor-pointer hover:opacity-80 transition-opacity" onClick={() => toggleDoor');

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log('patched doors');
