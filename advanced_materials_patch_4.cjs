const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// For Shutters
content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Shutter Door/g,
  `const sh = getCustomMat('shutter', rateToUse);
        pieces.push({
          customCostPerSqFt: sh.cost,
          label: \`Shutter Door\${sh.append}\``
);

content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Small Box Shutters/g,
  `const sh = getCustomMat('shutter', rateToUse);
          pieces.push({
            customCostPerSqFt: sh.cost,
            label: \`Small Box Shutters\${sh.append}\``
);

content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Double Shutter Door/g,
  `const sh = getCustomMat('shutter', rateToUse);
        pieces.push({
          customCostPerSqFt: sh.cost,
          label: \`Double Shutter Door\${sh.append}\``
);

content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Glass Shutter Door Frame/g,
  `const sh = getCustomMat('shutter', rateToUse);
        pieces.push({
          customCostPerSqFt: sh.cost,
          label: \`Glass Shutter Door Frame\${sh.append}\``
);


// For Drawer Faces
content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Drawer Face/g,
  `const df = getCustomMat('shutter', rateToUse);
        pieces.push({
          customCostPerSqFt: df.cost,
          label: \`Drawer Face\${df.append}\``
);
content = content.replace(
  /pieces\.push\(\{[\s]*label: "Drawer Face"/g,
  `const df = getCustomMat('shutter', rateToUse);
    pieces.push({
      customCostPerSqFt: df.cost,
      label: "Drawer Face" + df.append`
);

// For Drawer Side Panels
content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Drawer Side Panels/g,
  `const dbSide = getCustomMat('drawer', rateToUse);
          pieces.push({
            customCostPerSqFt: dbSide.cost,
            label: \`Drawer Side Panels\${dbSide.append}\``
);
content = content.replace(
  /pieces\.push\(\{[\s]*label: "Drawer Side Panels"/g,
  `const dbSide = getCustomMat('drawer', rateToUse);
    pieces.push({
      customCostPerSqFt: dbSide.cost,
      label: "Drawer Side Panels" + dbSide.append`
);

// For Drawer Inner Front/Back
content = content.replace(
  /pieces\.push\(\{[\s]*label: \`Drawer Inner Front\/Back/g,
  `const dbSide = getCustomMat('drawer', rateToUse);
          pieces.push({
            customCostPerSqFt: dbSide.cost,
            label: \`Drawer Inner Front/Back\${dbSide.append}\``
);
content = content.replace(
  /pieces\.push\(\{[\s]*label: "Drawer Inner Front\/Back"/g,
  `const dbSide = getCustomMat('drawer', rateToUse);
    pieces.push({
      customCostPerSqFt: dbSide.cost,
      label: "Drawer Inner Front/Back" + dbSide.append`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched dynamic items");
