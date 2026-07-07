import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_ui = """              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Wire Management
                </label>
                <select
                  value={wireManagement}
                  onChange={(e) => setWireManagement(e.target.value)}
                  className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                >
                  <option value="none">None</option>
                  
                  <option value="raceway">
                    Aluminum Flap Box (₹{WIRE_MANAGER_COST})
                  </option>
                  <option value="wire_raceway">
                    Metal Wire Raceway Tray (₹{METAL_RACEWAY_COST})
                  </option>
                </select>
              </div>"""

new_ui = """              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Wire Management
                </label>
                <div className="flex flex-col gap-2">
                  <select
                    value={wireManagement}
                    onChange={(e) => setWireManagement(e.target.value)}
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                  >
                    <option value="none">None</option>
                    
                    <option value="raceway">
                      Aluminum Flap Box
                    </option>
                    <option value="wire_raceway">
                      Metal Wire Raceway Tray (₹{METAL_RACEWAY_COST})
                    </option>
                  </select>
                  {wireManagement === "raceway" && (
                    <select
                      value={flapBoxRate}
                      onChange={(e) => setFlapBoxRate(Number(e.target.value))}
                      className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all text-sm"
                    >
                      {FLAP_BOX_RATES.map((rate) => (
                        <option key={rate} value={rate}>
                          ₹{rate} (per person)
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              </div>"""
content = content.replace(old_ui, new_ui)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
