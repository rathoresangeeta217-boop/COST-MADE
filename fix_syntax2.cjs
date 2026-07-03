const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// Fix `sh` redeclaration by replacing all `const sh = ...` with block scoping, or just reusing `sh`?
// Let's replace `const sh = getCustomMat('shutter', rateToUse);` with `let _sh = getCustomMat('shutter', rateToUse);` then `const sh = ...` with `_sh = ...`?
// No, the easiest is to just use block scope: `{ const sh = ...; pieces.push(...) }`
// Actually, let's just make it `let custom_sh = getCustomMat('shutter', rateToUse);` at the top of the loop?
// Wait, `const sh = getCustomMat('shutter', rateToUse);` appears right before `pieces.push({`.
// Let's just wrap it:
content = content.replace(/const sh = getCustomMat\('shutter', rateToUse\);\s*pieces\.push\(\{/g, `pieces.push({\n...getCustomMat('shutter', rateToUse), `);

// Wait, the object needs `customCostPerSqFt` and `label`. We can't just spread.
content = content.replace(/const sh = getCustomMat\('shutter', rateToUse\);\s*pieces\.push\(\{\s*customCostPerSqFt: sh\.cost,/g, 
  `pieces.push({\ncustomCostPerSqFt: getCustomMat('shutter', rateToUse).cost,`);

content = content.replace(/\$\{sh\.append\}/g, `\${getCustomMat('shutter', rateToUse).append}`);

// For df
content = content.replace(/const df = getCustomMat\('shutter', rateToUse\);\s*pieces\.push\(\{\s*customCostPerSqFt: df\.cost,/g, 
  `pieces.push({\ncustomCostPerSqFt: getCustomMat('shutter', rateToUse).cost,`);
content = content.replace(/\$\{df\.append\}/g, `\${getCustomMat('shutter', rateToUse).append}`);
// also fix the one that has `df.append` + "s"
content = content.replace(/label: \`Drawer Face\$\{getCustomMat\('shutter', rateToUse\)\.append\}\`s \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Drawer Faces (Bay ${index + 1})${getCustomMat('shutter', rateToUse).append}`,");


// For dbSide
content = content.replace(/const dbSide = getCustomMat\('drawer', rateToUse\);\s*pieces\.push\(\{\s*customCostPerSqFt: dbSide\.cost,/g, 
  `pieces.push({\ncustomCostPerSqFt: getCustomMat('drawer', rateToUse).cost,`);
content = content.replace(/\$\{dbSide\.append\}/g, `\${getCustomMat('drawer', rateToUse).append}`);

// Also string concatenation like "Drawer Face" + df.append
content = content.replace(/ \+ df\.append/g, ` + getCustomMat('shutter', rateToUse).append`);
content = content.replace(/ \+ dbSide\.append/g, ` + getCustomMat('drawer', rateToUse).append`);


fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Syntax 2 fixed");
