import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_layout_ui = """              <div>
                <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1 whitespace-nowrap">
                  Layout
                </label>
                <select
                  value={layout}
                  onChange={(e) => setLayout(e.target.value)}
                  className="block w-full px-2 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900 font-medium text-sm"
                >
                  <option value="linear">Linear</option>
                  <option value="back_to_back">Back-to-Back</option>
                </select>
              </div>"""

new_layout_ui = """              <div>
                <label className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1 whitespace-nowrap">
                  Layout
                </label>
                <select
                  value={layout}
                  onChange={(e) => setLayout(e.target.value)}
                  className="block w-full px-2 py-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900 font-medium text-sm"
                >
                  <option value="linear">Linear</option>
                  <option value="back_to_back">Back-to-Back</option>
                </select>
                {layout === "linear" && (
                  <label className="flex items-start gap-1.5 mt-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={isHeightAdjustable}
                      onChange={(e) => setIsHeightAdjustable(e.target.checked)}
                      className="w-3.5 h-3.5 mt-0.5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="text-[10px] font-medium text-gray-600 leading-tight">Height Adjustable</span>
                  </label>
                )}
              </div>"""

content = content.replace(old_layout_ui, new_layout_ui)
with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
