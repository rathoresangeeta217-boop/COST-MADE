const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// 1. Remove isFullScreenDrawing check for AnimatedDoorGroup onClick
content = content.replace(/onClick=\{\(\) \=\> isFullScreenDrawing \&\& toggleDoor/g, 'onClick={() => toggleDoor');
content = content.replace(/className=\{isFullScreenDrawing \? "cursor-pointer hover:opacity-80 transition-opacity" : ""\}/g, 'className="cursor-pointer hover:opacity-80 transition-opacity"');

// 2. Remove isFullScreenDrawing check in renderShelves
content = content.replace(/className=\{isFullScreenDrawing \? \(dragState\?\.partitionId === pId \? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity"\) : ""\}/g, 'className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity"}');

content = content.replace(/if \(\!isFullScreenDrawing\) return;\n/g, '');

content = content.replace(/\{isFullScreenDrawing \&\& \<line x1=\{sX1\} y1=\{sY\} x2=\{sX2\} y2=\{sY\} stroke="transparent" strokeWidth="15" \/\>\}/g, '<line x1={sX1} y1={sY} x2={sX2} y2={sY} stroke="transparent" strokeWidth="15" />');
content = content.replace(/\{isFullScreenDrawing \&\& \<line x1=\{vX\} y1=\{vY1\} x2=\{vX\} y2=\{vY2\} stroke="transparent" strokeWidth="15" \/\>\}/g, '<line x1={vX} y1={vY1} x2={vX} y2={vY2} stroke="transparent" strokeWidth="15" />');

content = content.replace(/stroke=\{isRemoved \? \(isFullScreenDrawing \? "rgba\(71,85,105,0\.3\)" : "transparent"\) : "\#475569"\}/g, 'stroke={isRemoved ? "rgba(71,85,105,0.3)" : "#475569"}');

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Made drawing always interactive");
