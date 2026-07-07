const fs = require('fs');

let content = fs.readFileSync('src/pages/WorkstationCalculator.tsx', 'utf8');

// 1. Add to calculateWorkstationCost parameters
content = content.replace(
  /metalLegPipeSize,\n  screenId,\n  screenHeight,/,
  `metalLegPipeSize,\n  screenId,\n  screenHeight,\n  screenLayout = "end_to_end",`
);

// 2. Add effectiveScreenWidth inside calculateWorkstationCost (around line 206, after innerRate etc)
content = content.replace(
  /const totalMicaRate = innerRate \+ outerRate;\n\n  \/\/ Workstation Layout Math/,
  `const totalMicaRate = innerRate + outerRate;\n\n  const effectiveScreenWidth = screenLayout === "in_blocks" ? Math.max(0, width - 100) : width;\n\n  // Workstation Layout Math`
);

// 3. Update sAreaSqFt logic
content = content.replace(
  /const sAreaSqFt = \(width \* screenHeight \* screenCount\) \/ 90000;/,
  `const sAreaSqFt = (effectiveScreenWidth * screenHeight * screenCount) / 90000;`
);

// 4. Update screen board sqft logic
content = content.replace(
  /\(screenId === "board" \? width \* screenHeight \* cols : 0\)/,
  `(screenId === "board" ? effectiveScreenWidth * screenHeight * cols : 0)`
);

// 5. Add state
content = content.replace(
  /const \[screenId, setScreenId\] = useState<string>\("none"\);/,
  `const [screenId, setScreenId] = useState<string>("none");\n  const [screenLayout, setScreenLayout] = useState<string>("end_to_end");`
);

// 6. Update loader
content = content.replace(
  /if \(c\.screenId !== undefined\) setScreenId\(c\.screenId\);/,
  `if (c.screenId !== undefined) setScreenId(c.screenId);\n        if (c.screenLayout !== undefined) setScreenLayout(c.screenLayout);`
);

// 7. Update calculateWorkstationCost call
content = content.replace(
  /metalLegPipeSize,\n      screenId,\n      screenHeight,/,
  `metalLegPipeSize,\n      screenId,\n      screenHeight,\n      screenLayout,`
);

// 8. Update useMemo dependencies
content = content.replace(
  /metalLegPipeSize,\n    screenId,\n    screenHeight,/,
  `metalLegPipeSize,\n    screenId,\n    screenHeight,\n    screenLayout,`
);

// 9. Update itemData config
content = content.replace(
  /metalLegPipeSize, screenId, screenHeight,/,
  `metalLegPipeSize, screenId, screenHeight, screenLayout,`
);

// 10. Update UI to show the option
const uiInsert = `
                  {screenId !== "none" && (
                    <div className="flex gap-4 items-center mt-2">
                      <select
                        value={screenLayout}
                        onChange={(e) => setScreenLayout(e.target.value)}
                        className="w-1/2 px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                      >
                        <option value="end_to_end">End to End (Full Length)</option>
                        <option value="in_blocks">In Blocks (Less 100mm)</option>
                      </select>
                      <div className="w-1/2 flex items-center gap-2">
`;
content = content.replace(
  /\{screenId !== "none" && \(\n\s*<div className="flex items-center gap-2 mt-2">/,
  uiInsert
);

fs.writeFileSync('src/pages/WorkstationCalculator.tsx', content);
console.log("Patched screenLayout");
