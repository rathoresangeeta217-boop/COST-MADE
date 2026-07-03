const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// Add the showAdvancedMaterials state
content = content.replace(
  /const \[drawerBoxBoardId, setDrawerBoxBoardId\] = useState<string>\("default"\);/,
  `const [drawerBoxBoardId, setDrawerBoxBoardId] = useState<string>("default");\n  const [showAdvancedMaterials, setShowAdvancedMaterials] = useState<boolean>(false);`
);

// Add the UI
const advancedUI = `
            {/* Advanced Board Materials */}
            <div className="pt-2">
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-3 cursor-pointer">
                <input type="checkbox" checked={showAdvancedMaterials} onChange={e => setShowAdvancedMaterials(e.target.checked)} className="rounded text-indigo-600 focus:ring-indigo-500" />
                <span>Customize Material for specific parts</span>
              </label>
              
              {showAdvancedMaterials && (
                <div className="space-y-4 p-4 bg-gray-50 rounded-xl border border-gray-200">
                  
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Shutter / Doors Board Material
                    </label>
                    <select
                      value={shutterBoardId}
                      onChange={(e) => setShutterBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Same as Carcass Board ({activeBoard.name})</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Back Panel Board Material (9mm)
                    </label>
                    <select
                      value={backPanelBoardId}
                      onChange={(e) => setBackPanelBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Standard 9mm PLPB Backing (₹35/sq.ft)</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, 9, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Drawer Box Panels (9mm)
                    </label>
                    <select
                      value={drawerBoxBoardId}
                      onChange={(e) => setDrawerBoxBoardId(e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                    >
                      <option value="default">Standard Drawer Panels</option>
                      {boards.map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, 9, quality)}/sq.ft)
                        </option>
                      ))}
                    </select>
                  </div>

                </div>
              )}
            </div>
`;

content = content.replace(
  /<\/select>\n\s*<\/div>\n\s*<\/div>/,
  `</select>\n              </div>\n            </div>\n\n${advancedUI}`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched UI");
