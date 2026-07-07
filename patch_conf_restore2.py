import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

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

# Replace from {/* Add-ons */} to the END of that section
content = re.sub(r'\{\/\* Add-ons \*\/}.*?<\/section>', addons_replacement, content, flags=re.DOTALL)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
