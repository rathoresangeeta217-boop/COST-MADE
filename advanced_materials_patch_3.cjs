const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// 1. Back panel
content = content.replace(
  /pieces\.push\(\{[\s]*label: "Back Panel \(9mm PLPB Backing\)",[\s]*w: width,[\s]*l: height,[\s]*qty: 1,[\s]*customCostPerSqFt: 35,[\s]*ebMm: 0,[\s]*\}\);/g,
  `const bp = getCustomMat('back', 35, ' (9mm PLPB Backing)');
    pieces.push({
      label: "Back Panel" + bp.append,
      w: width,
      l: height,
      qty: 1,
      customCostPerSqFt: bp.cost,
      ebMm: 0,
    });`
);

// 2. Drawer Bottom Panels
content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Drawer Bottom Panels \(Bay \$\{index \+ 1\}\)\`,[\s]*w: dw,[\s]*l: dd,[\s]*qty: bayDrawers,[\s]*customCostPerSqFt: 35,[\s]*ebMm: 0,[\s]*\}\);/g,
  `const dbBottom = getCustomMat('drawer', 35);
          pieces.push({
            label: \`Drawer Bottom Panels (Bay \${index + 1})\` + dbBottom.append,
            w: dw,
            l: dd,
            qty: bayDrawers,
            customCostPerSqFt: dbBottom.cost,
            ebMm: 0,
          });`
);

content = content.replace(
  /pieces\.push\(\{[\s]*label: "Drawer Bottom Panel",[\s]*w: boxWidth,[\s]*l: boxDepth,[\s]*qty: 1,[\s]*customCostPerSqFt: 35, \/\/ PLPB backing[\s]*ebMm: 0,[\s]*\}\);/g,
  `const dbBottom = getCustomMat('drawer', 35);
    pieces.push({
      label: "Drawer Bottom Panel" + dbBottom.append,
      w: boxWidth,
      l: boxDepth,
      qty: 1,
      customCostPerSqFt: dbBottom.cost,
      ebMm: 0,
    });`
);

// 3. Replace all Drawer Faces and Shutters with the custom cost
// Wait, we can just replace 'pieces.push({' with a slightly modified version, but that's risky.

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched 1");
