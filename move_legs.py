import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# Remove the current Number of Leg Panels block
block_to_remove = """                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Leg Panels / Frames
                  </label>
                  <input
                    type="number"
                    value={legCountOverride === 0 ? '' : legCountOverride}
                    onChange={(e) => setLegCountOverride(Number(e.target.value) || 0)}
                    placeholder="Auto (based on layout)"
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                    min="0"
                  />
                </div>"""

content = content.replace(block_to_remove, '')

# Find the Understructure block and insert it after it
understructure_block = """                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Understructure (Legs)
                  </label>
                  <select
                    value={legId}
                    onChange={(e) => setLegId(e.target.value)}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                  >
                    {LEGS.map((l) => (
                      <option key={l.id} value={l.id}>
                        {l.name}
                      </option>
                    ))}
                  </select>
                </div>"""

new_leg_count = """                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Custom Leg Count (Override)
                  </label>
                  <input
                    type="number"
                    value={legCountOverride === 0 ? '' : legCountOverride}
                    onChange={(e) => setLegCountOverride(Number(e.target.value) || 0)}
                    placeholder="Auto calculation"
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                    min="0"
                  />
                </div>"""

content = content.replace(understructure_block, understructure_block + '\n' + new_leg_count)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
