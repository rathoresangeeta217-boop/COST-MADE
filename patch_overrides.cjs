const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// 1. Add state
content = content.replace(
  /const \[drawerBoxBoardId, setDrawerBoxBoardId\] = useState<string>\("default"\);/,
  `const [drawerBoxBoardId, setDrawerBoxBoardId] = useState<string>("default");\n  const [pieceOverrides, setPieceOverrides] = useState<Record<string, string>>({});`
);

// 2. Add to loader
content = content.replace(
  /if \(c\.drawerBoxBoardId !== undefined\) setDrawerBoxBoardId\(c\.drawerBoxBoardId\);/,
  `if (c.drawerBoxBoardId !== undefined) setDrawerBoxBoardId(c.drawerBoxBoardId);\n        if (c.pieceOverrides !== undefined) setPieceOverrides(c.pieceOverrides);`
);

// 3. Add to itemData
content = content.replace(
  /bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId\n\s*\},/,
  `bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId, pieceOverrides\n                  },`
);

// 4. In calcData and drawerCalcData dependencies, add pieceOverrides
content = content.replace(
  /shutterBoardId, backPanelBoardId, drawerBoxBoardId\]\);/g,
  `shutterBoardId, backPanelBoardId, drawerBoxBoardId, pieceOverrides]);`
);
content = content.replace(
  /drawerBoxBoardId, shutterBoardId\]\);/g,
  `drawerBoxBoardId, shutterBoardId, pieceOverrides]);`
);

// 5. In calcData and drawerCalcData, intercept itemRate
content = content.replace(
  /const itemRate = p\.customCostPerSqFt \?\? rateToUse;/g,
  `      const overrideLabel = p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '');
      const overrideId = pieceOverrides[overrideLabel];
      let itemRate = p.customCostPerSqFt ?? rateToUse;
      if (overrideId && overrideId !== 'default') {
          const customB = boards.find(x => x.id === overrideId);
          if (customB) {
            let t = boardThickness;
            if (overrideLabel.includes('Back') || overrideLabel.includes('Bottom') || overrideLabel.includes('Inner')) t = 9;
            itemRate = getBoardRate(overrideId, customB.costPerSqFt, t, quality);
            if (overrideLabel.includes('Shutter') || overrideLabel.includes('Drawer Face')) itemRate += totalMicaRate;
            p.label = overrideLabel + \` (\${customB.name} \${t}mm)\`;
          }
      }`
);

// 6. In the table, render the dropdown
content = content.replace(
  /<th className="p-3 text-right">Size \(mm\)<\/th>/g,
  `<th className="p-3 text-right">Size (mm)</th>\n                    <th className="p-3 text-left">Board Material</th>`
);

content = content.replace(
  /<td className="p-3 text-right">\{p\.w\} x \{p\.l\}<\/td>/g,
  `<td className="p-3 text-right">{p.w} x {p.l}</td>\n                      <td className="p-3 text-left">\n                        <select\n                          value={pieceOverrides[p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '')] || 'default'}\n                          onChange={(e) => setPieceOverrides({...pieceOverrides, [p.label.replace(/\\s\\([^)]*(mm|Backing)\\)$/, '')]: e.target.value})}\n                          className="px-2 py-1 bg-white border border-gray-200 rounded text-xs outline-none focus:border-indigo-500 w-32"\n                        >\n                          <option value="default">Default</option>\n                          {boards.map(b => (\n                            <option key={b.id} value={b.id}>{b.name}</option>\n                          ))}\n                        </select>\n                      </td>`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched overrides");
