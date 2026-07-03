const fs = require('fs');

function patchFile(filename) {
    let content = fs.readFileSync(filename, 'utf-8');
    content = content.replace(
        /const LEGS = \[\s*\{ id: "board", name: "Board\/Wooden Legs", cost: 0 \},[\s\S]*?\];/,
        `const LEGS = [
  { id: "board", name: "Board/Wooden Legs", cost: 0 },
  { id: "metal_leg", name: "Metal Legs", cost: 1500 },
];`
    );
    fs.writeFileSync(filename, content);
}

patchFile('src/pages/WorkstationCalculator.tsx');
patchFile('src/pages/LShapeTableCalculator.tsx');
console.log("Patched legs");
