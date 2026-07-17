import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

metal_bays_ui = """          {/* Section 2: Columns Partition Builder */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex flex-wrap items-center justify-between border-b border-gray-100 pb-3 gap-4">
              <div className="flex items-center gap-2">
                <LayoutGrid className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  2. {constructionCategory === "wooden" ? "Columns & Internal Layout" : "Shelving Configuration"}
                </h2>
              </div>
            </div>

            {constructionCategory === "metal" ? (
              <div className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1.5">
                      Number of Horizontal Bays (Rows)
                    </label>
                    <input
                      type="number"
                      min={1}
                      max={20}
                      value={numRows}
                      onChange={(e) => setNumRows(Number(e.target.value))}
                      className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div className="flex items-center pt-5">
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addVerticalPartitionMiddle}
                        onChange={(e) => setAddVerticalPartitionMiddle(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Vertical Partition at Middle
                    </label>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-4">"""

content = re.sub(
    r'          \{\/\* Section 2: Columns Partition Builder \*\/.*?<\/h2>\n              <\/div>\n              <div className="flex items-center gap-4">',
    metal_bays_ui,
    content,
    flags=re.DOTALL
)

content = content.replace(
    "              })}\n            </div>\n          </div>\n\n          {/* Section 3:",
    "              })}\n            </div>\n              </>\n            )}\n          </div>\n\n          {/* Section 3:"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
