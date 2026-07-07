const fs = require('fs');
let content = fs.readFileSync('src/pages/WorkstationCalculator.tsx', 'utf8');

const target = 'const sideBracketCount = (depth > 600 ? 3 : 2) * sideScreenCount;';
const replacement = 'const sideBracketCount = (effectiveSideDepth > 600 ? 3 : 2) * sideScreenCount;';

if (content.includes(target)) {
    content = content.replace(target, replacement);
    fs.writeFileSync('src/pages/WorkstationCalculator.tsx', content);
    console.log("Patched side brackets");
} else {
    console.log("Could not find target");
}
