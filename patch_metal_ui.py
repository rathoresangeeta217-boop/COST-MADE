import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

wooden_material_ui = """            {/* Board Material and Thickness Selection */}
            {constructionCategory === "wooden" ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Carcass Board Material
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
                  Board Thickness
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
            ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Slotted Angle Material
                </label>
                <select
                  value={boardId}
                  onChange={(e) => setBoardId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  {boards.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.name} (₹{getBoardRate(b.id, b.costPerSqFt, angleThickness, quality)}/sq.ft)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Angle Thickness (Gage)
                </label>
                <select
                  value={angleThickness}
                  onChange={(e) => setAngleThickness(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                >
                  {getAvailableThicknesses(boardId, quality).map((t) => (
                    <option key={t} value={t}>
                      {t} mm
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="sm:col-span-2 pt-2 border-t border-gray-100 mt-2">
                <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Shelf Configuration</span>
              </div>
              
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Shelf Material Type
                </label>
                <select
                  value={shelfMaterialType}
                  onChange={(e) => setShelfMaterialType(e.target.value as "metal" | "wooden")}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  <option value="metal">Metal Shelves</option>
                  <option value="wooden">Wooden Shelves</option>
                </select>
              </div>
              
              {shelfMaterialType === "metal" ? (
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Metal Shelf Thickness
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
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Wooden Material
                    </label>
                    <select
                      value={woodenShelfId}
                      onChange={(e) => setWoodenShelfId(e.target.value)}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getBoards(quality, "wooden").map((b) => (
                        <option key={b.id} value={b.id}>
                          {b.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Thickness
                    </label>
                    <select
                      value={woodenShelfThickness}
                      onChange={(e) => setWoodenShelfThickness(Number(e.target.value))}
                      className="w-full px-2 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 outline-none"
                    >
                      {getAvailableThicknesses(woodenShelfId, quality).map((t) => (
                        <option key={t} value={t}>
                          {t} mm
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}
            </div>
            )}"""

# Replace the existing Board Material and Thickness Selection block
content = re.sub(
    r'            \{\/\* Board Material and Thickness Selection \*\/.*?<\/div>\n            <\/div>',
    wooden_material_ui,
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
