const fs = require('fs');

const files = ['src/pages/WorkstationCalculator.tsx', 'src/pages/LShapeTableCalculator.tsx'];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  
  // 1. Add to calculate parameter
  content = content.replace(
    /modestyType( = "standard")?,\n\s*cncDesignOnModesty/g,
    `modestyType$1,\n  modestyFinish = "plain",\n  cncDesignOnModesty`
  );

  // 2. Add to bDetails label in modesty section
  // we need to find the place where it pushes modesty panel
  // "label: `Modesty Panel (" + modestyType + ")`" or similar
  content = content.replace(
    /label: \`Modesty Panel \((.*?)\)\`/g,
    `label: \`Modesty Panel ($1, \${modestyFinish})\``
  );
  content = content.replace(
    /label: \`Modesty Panel \((.*?)\)\`/g,
    `label: \`Modesty Panel ($1, \${modestyFinish})\``
  );

  // For metal leg modesty, it's already "Metal Modesty Panel (Plain | CNC)". We won't touch that unless it's board.
  
  // 3. Add to state
  content = content.replace(
    /const \[modestyType, setModestyType\] = useState<string>\("standard"\);/g,
    `const [modestyType, setModestyType] = useState<string>("standard");\n  const [modestyFinish, setModestyFinish] = useState<string>("plain");`
  );

  // 4. Update loader
  content = content.replace(
    /if \(c\.modestyType !== undefined\) setModestyType\(c\.modestyType\);/g,
    `if (c.modestyType !== undefined) setModestyType(c.modestyType);\n        if (c.modestyFinish !== undefined) setModestyFinish(c.modestyFinish);`
  );

  // 5. Update calculateWorkstationCost / calculateLShapeTableCost call
  content = content.replace(
    /modestyType,\n\s*cncDesignOnModesty,/g,
    `modestyType,\n      modestyFinish,\n      cncDesignOnModesty,`
  );
  
  // Update useMemo
  content = content.replace(
    /modestyType,\n\s*cncDesignOnModesty,/g,
    `modestyType,\n    modestyFinish,\n    cncDesignOnModesty,`
  );
  
  // Update export
  content = content.replace(
    /modestyType: exportModestyType,\n\s*cncDesignOnModesty:/g,
    `modestyType: exportModestyType,\n              modestyFinish: "plain",\n              cncDesignOnModesty:`
  );

  // Update itemData config
  content = content.replace(
    /includeModesty, modestyType, cncDesignOnModesty,/g,
    `includeModesty, modestyType, modestyFinish, cncDesignOnModesty,`
  );

  // Update UI
  const uiSearch = `                  {includeModesty && legId === "board" && (
                    <div className="flex gap-4">
                      <select`;
  // if not found, try the other pattern
  const uiSearchAlt = `{includeModesty && legId === "board" && (
                      <div className="ml-8 mt-1">
                        <select
                          value={modestyType}`;
  const uiReplaceAlt = `{includeModesty && legId === "board" && (
                      <div className="ml-8 mt-1 flex gap-2">
                        <select
                          value={modestyType}`;
  
  content = content.replace(uiSearchAlt, uiReplaceAlt);
  
  const uiSearch2 = `                          <option value="shorter">Very Short (300 mm)</option>
                        </select>
                      </div>
                    )}`;
  const uiReplace2 = `                          <option value="shorter">Very Short (300 mm)</option>
                        </select>
                        <select
                          value={modestyFinish}
                          onChange={(e) => setModestyFinish(e.target.value)}
                          className="block w-full max-w-xs px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                          <option value="plain">Plain</option>
                          <option value="fluted">Fluted</option>
                        </select>
                      </div>
                    )}`;
  content = content.replace(uiSearch2, uiReplace2);

  fs.writeFileSync(file, content);
}
console.log("Patched modesty finish");
