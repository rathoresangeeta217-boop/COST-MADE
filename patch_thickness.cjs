const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// 1. Add state
content = content.replace(
  /const \[pieceOverrides, setPieceOverrides\] = useState<Record<string, string>>\(\{\}\);/,
  `const [pieceOverrides, setPieceOverrides] = useState<Record<string, string>>({});\n  const [thicknessOverrides, setThicknessOverrides] = useState<Record<string, number>>({});`
);

// 2. Add to loader
content = content.replace(
  /if \(c\.pieceOverrides !== undefined\) setPieceOverrides\(c\.pieceOverrides\);/,
  `if (c.pieceOverrides !== undefined) setPieceOverrides(c.pieceOverrides);\n        if (c.thicknessOverrides !== undefined) setThicknessOverrides(c.thicknessOverrides);`
);

// 3. Add to itemData
content = content.replace(
  /pieceOverrides\n\s*\},/,
  `pieceOverrides, thicknessOverrides\n                  },`
);

// 4. Dependencies
content = content.replace(
  /pieceOverrides\]\);/g,
  `pieceOverrides, thicknessOverrides]);`
);

// 5. Intercept logic update
const newIntercept = `
      const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');
      const overrideId = pieceOverrides[overrideLabel];
      const overrideThickness = thicknessOverrides[overrideLabel];
      let itemRate = p.customCostPerSqFt ?? rateToUse;
      
      let baseId = boardId;
      if (overrideLabel.includes('Shutter') || overrideLabel.includes('Drawer Face')) baseId = shutterBoardId !== 'default' ? shutterBoardId : boardId;
      else if (overrideLabel.includes('Back')) baseId = backPanelBoardId !== 'default' ? backPanelBoardId : boardId;
      else if (overrideLabel.includes('Drawer')) baseId = drawerBoxBoardId !== 'default' ? drawerBoxBoardId : boardId;
      
      let currentId = (overrideId && overrideId !== 'default') ? overrideId : baseId;
      
      if ((overrideId && overrideId !== 'default') || overrideThickness) {
          const customB = boards.find(x => x.id === currentId);
          if (customB) {
            let defaultT = boardThickness;
            if (overrideLabel.includes('Back') || overrideLabel.includes('Bottom') || overrideLabel.includes('Inner')) defaultT = 9;
            
            const t = overrideThickness || defaultT;
            itemRate = getBoardRate(currentId, customB.costPerSqFt, t, quality);
            if (overrideLabel.includes('Shutter') || overrideLabel.includes('Drawer Face')) itemRate += totalMicaRate;
            p.label = overrideLabel + \` (\${customB.name} \${t}mm)\`;
          }
      }
      const itemCost = totalSqFt * itemRate;

      if (p.customCostPerSqFt) {
`;

// we need to find the exact block to replace.
const split1 = content.split("const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');");
if (split1.length === 3) {
  // It occurs twice: once in calcData and once in drawerCalcData.
  for(let i=1; i<=2; i++) {
     let block = split1[i];
     let endIndex = block.indexOf("if (p.customCostPerSqFt) {");
     split1[i] = newIntercept.replace("const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');\\n", "") + block.substring(endIndex + "if (p.customCostPerSqFt) {".length);
  }
  content = split1.join("const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');");
} else {
  console.log("Could not find the block to replace, found splits:", split1.length);
}

// 6. Update table headers
content = content.replace(
  /<th className="p-3 text-left">Board Material<\/th>/g,
  `<th className="p-3 text-left">Board Material</th>\n                    <th className="p-3 text-left">Thickness</th>`
);

// 7. Update table body
const dropdownHTML = `                      <td className="p-3 text-left">
                        <select
                          value={thicknessOverrides[p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '')] || ''}
                          onChange={(e) => {
                            const val = e.target.value;
                            if (val) {
                                setThicknessOverrides({...thicknessOverrides, [p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '')]: Number(val)});
                            } else {
                                const newOver = {...thicknessOverrides};
                                delete newOver[p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '')];
                                setThicknessOverrides(newOver);
                            }
                          }}
                          className="px-2 py-1 bg-white border border-gray-200 rounded text-xs outline-none focus:border-indigo-500 w-20"
                        >
                          <option value="">Default</option>
                          {[6, 9, 12, 18, 25].map(t => (
                            <option key={t} value={t}>{t} mm</option>
                          ))}
                        </select>
                      </td>`;
content = content.replace(
  /<\/select>\n\s*<\/td>/g,
  `</select>\n                      </td>\n${dropdownHTML}`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched thickness overrides");
