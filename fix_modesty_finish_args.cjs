const fs = require('fs');
let file = 'src/pages/LShapeTableCalculator.tsx';
let content = fs.readFileSync(file, 'utf8');

const search = `  modestyType = "standard",
  metalModestyType = "plain",`;
const replace = `  modestyType = "standard",
  modestyFinish = "plain",
  metalModestyType = "plain",`;

if (content.includes(search)) {
  content = content.replace(search, replace);
  fs.writeFileSync(file, content);
  console.log("Fixed args in LShapeTableCalculator");
} else {
  console.log("Could not find search block in LShapeTableCalculator");
}
