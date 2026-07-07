import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

ui_replacement = """              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Leg Type</label>
                  <select
                    value={legType}
                    onChange={(e) => setLegType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <optgroup label="Metal Legs">
                      <option value="metal_straight">Straight Legs</option>
                      <option value="metal_u">U-Shape Leg</option>
                    </optgroup>
                    <optgroup label="Board Legs">
                      <option value="board">Same as Table</option>
                      <option value="box_plain">Box Legs (Plain)</option>
                      <option value="box_fluted">Box Legs (Fluted)</option>
                      <option value="round_plain">Round Leg (Plain)</option>
                      <option value="round_fluted">Round Leg (Fluted)</option>
                    </optgroup>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Leg Count</label>
                  <select
                    value={legCountInput}
                    onChange={(e) => setLegCountInput(Number(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <option value={0}>Auto (Based on Width)</option>
                    <option value={2}>2 Legs</option>
                    <option value={3}>3 Legs</option>
                    <option value={4}>4 Legs</option>
                    <option value={5}>5 Legs</option>
                    <option value={6}>6 Legs</option>
                  </select>
                </div>
              </div>"""

content = re.sub(
    r'<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">.*?</div>\n              </div>',
    ui_replacement,
    content,
    flags=re.DOTALL
)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
