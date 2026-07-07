import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

wire_management_replacement = """            {/* Wire Management */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-indigo-500" />
                Wire Management
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Type</label>
                  <select
                    value={wireManagement}
                    onChange={(e) => setWireManagement(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                  >
                    <option value="none">None</option>
                    <option value="aluminum_flip_box">Aluminum Flip Box</option>
                    <option value="wire_raceway">Wire Raceway</option>
                  </select>
                </div>
              </div>
            </section>"""

addons_replacement = """            {/* Add-ons */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-500" />
                Add-ons
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl bg-gray-50/50">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 rounded-lg">
                      <Sparkles className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Leatherlite Design Pad</p>
                      <p className="text-xs text-gray-500">Premium center insert</p>
                    </div>
                  </div>
                  <Switch checked={addLeatherlite} onCheckedChange={setAddLeatherlite} />
                </div>
              </div>
            </section>"""

# Find the second instance of <div className="grid grid-cols-1 sm:grid-cols-2 gap-4"> inside Wire Management section
content = re.sub(r'\{\/\* Wire Management \*\/}.*?<\/section>', wire_management_replacement, content, flags=re.DOTALL)

# Find the Add-ons section
content = re.sub(r'\{\/\* Add-ons \*\/}.*?<\/section>', addons_replacement, content, flags=re.DOTALL)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
