const fs = require('fs');
let content = fs.readFileSync('src/pages/WorkstationCalculator.tsx', 'utf8');

const uiSearch = `                  {screenId !== "none" && (
                    <select
                      value={screenHeight}`;

const uiReplace = `                  {screenId !== "none" && (
                    <div className="flex flex-col gap-2 w-1/2">
                    <select
                      value={screenHeight}`;

content = content.replace(uiSearch, uiReplace);

const uiSearch2 = `                      <option value={450}>450 mm High</option>
                    </select>
                  )}`;

const uiReplace2 = `                      <option value={450}>450 mm High</option>
                    </select>
                    <select
                        value={screenLayout}
                        onChange={(e) => setScreenLayout(e.target.value)}
                        className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                      >
                        <option value="end_to_end">End to End (Full Length)</option>
                        <option value="in_blocks">In Blocks (Less 100mm)</option>
                      </select>
                    </div>
                  )}`;

content = content.replace(uiSearch2, uiReplace2);

fs.writeFileSync('src/pages/WorkstationCalculator.tsx', content);
console.log("Patched UI");
