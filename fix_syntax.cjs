const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// The invalid syntax is: label: `TEXT${append}` (Bay ${index + 1})`,
// We want to turn it into: label: `TEXT (Bay ${index + 1})${append}`,

content = content.replace(/label: \`Small Box Shutters\$\{sh\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Small Box Shutters (Bay ${index + 1})${sh.append}`,");

content = content.replace(/label: \`Shutter Door\$\{sh\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Shutter Door (Bay ${index + 1})${sh.append}`,");

content = content.replace(/label: \`Double Shutter Door\$\{sh\.append\}\` \(Bay \$\{index \+ 1\} - Left\)\`,/g, 
  "label: `Double Shutter Door (Bay ${index + 1} - Left)${sh.append}`,");

content = content.replace(/label: \`Double Shutter Door\$\{sh\.append\}\` \(Bay \$\{index \+ 1\} - Right\)\`,/g, 
  "label: `Double Shutter Door (Bay ${index + 1} - Right)${sh.append}`,");

content = content.replace(/label: \`Glass Shutter Door Frame\$\{sh\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Glass Shutter Door Frame (Bay ${index + 1})${sh.append}`,");

content = content.replace(/label: \`Drawer Faces\$\{df\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Drawer Faces (Bay ${index + 1})${df.append}`,");

content = content.replace(/label: \`Drawer Face\$\{df\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Drawer Face (Bay ${index + 1})${df.append}`,");

content = content.replace(/label: \`Drawer Side Panels\$\{dbSide\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Drawer Side Panels (Bay ${index + 1})${dbSide.append}`,");

content = content.replace(/label: \`Drawer Inner Front\/Back\$\{dbSide\.append\}\` \(Bay \$\{index \+ 1\}\)\`,/g, 
  "label: `Drawer Inner Front/Back (Bay ${index + 1})${dbSide.append}`,");

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Syntax fixed");
