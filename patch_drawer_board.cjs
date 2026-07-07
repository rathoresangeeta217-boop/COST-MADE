const fs = require('fs');
let file = 'src/pages/CustomStorageCalculator.tsx';
let content = fs.readFileSync(file, 'utf8');

const target = `                  )}
                </div>
              </div>

              {/* Drawer Hardware Options */}`;

const replacement = `                  )}
                </div>
              </div>
              
              {/* Board Material and Thickness Selection */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Drawer Face Board Material
                  </label>
                  <select
                    value={boardId}
                    onChange={(e) => setBoardId(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                  >
                    {boards.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, boardThickness, quality)}/sq.ft)
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Drawer Face Thickness
                  </label>
                  <select
                    value={boardThickness}
                    onChange={(e) => setBoardThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    {getAvailableThicknesses(boardId, quality).map((t) => (
                      <option key={t} value={t}>
                        {t} mm
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Drawer Hardware Options */}`;

if (content.includes(target)) {
  content = content.replace(target, replacement);
  fs.writeFileSync(file, content);
  console.log("Patched CustomStorageCalculator.tsx");
} else {
  console.log("Could not find target");
}
