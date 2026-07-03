const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

const target = "const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');";

while (content.includes(target + "\n" + target)) {
  content = content.replace(target + "\n" + target, target);
}
while (content.includes(target + "\n      " + target)) {
  content = content.replace(target + "\n      " + target, target);
}
while (content.includes(target + "\n        " + target)) {
  content = content.replace(target + "\n        " + target, target);
}

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Fixed double overrideLabel");
