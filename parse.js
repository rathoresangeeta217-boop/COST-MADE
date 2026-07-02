const fs = require('fs');
const content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
const lines = content.split('\n');
lines.forEach((l, i) => {
  if (l.includes('AnimatedDoorGroup')) {
    console.log(i + 1 + ': ' + l.trim());
  }
});
