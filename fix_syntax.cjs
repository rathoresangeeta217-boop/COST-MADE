const fs = require('fs');

const files = ['src/pages/WorkstationCalculator.tsx', 'src/pages/LShapeTableCalculator.tsx'];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  
  content = content.replace(/const \[modestyFinish = "plain", setModestyFinish\] = useState<string>\("plain"\);/, 'const [modestyFinish, setModestyFinish] = useState<string>("plain");');
  
  content = content.replace(/modestyType,\n  modestyFinish = "plain",\n  cncDesignOnModesty,/g, 'modestyType,\n      modestyFinish,\n      cncDesignOnModesty,');
  
  content = content.replace(/includeModesty, modestyType, modestyFinish = "plain", cncDesignOnModesty,/g, 'includeModesty, modestyType, modestyFinish, cncDesignOnModesty,');

  fs.writeFileSync(file, content);
}
console.log("Fixed syntax");
