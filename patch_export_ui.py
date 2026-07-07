import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_ui = """              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">
                  Wire Management
                </label>
                <select
                  value={exportWireManagement}
                  onChange={(e) => setExportWireManagement(e.target.value)}
                  className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                >
                  <option value="none">None</option>
                  
                  <option value="raceway">Alu Flap Raceway</option>
                  <option value="wire_raceway">Metal Wire Raceway</option>
                </select>
              </div>"""

new_ui = """              <div className="space-y-2 p-3 border rounded-lg">
                <label className="text-sm font-medium text-gray-900">
                  Wire Management
                </label>
                <div className="flex flex-col gap-2">
                  <select
                    value={exportWireManagement}
                    onChange={(e) => setExportWireManagement(e.target.value)}
                    className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                  >
                    <option value="none">None</option>
                    
                    <option value="raceway">Alu Flap Box</option>
                    <option value="wire_raceway">Metal Wire Raceway</option>
                  </select>
                  {exportWireManagement === "raceway" && (
                    <select
                      value={exportFlapBoxRate}
                      onChange={(e) => setExportFlapBoxRate(Number(e.target.value))}
                      className="block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none"
                    >
                      {FLAP_BOX_RATES.map((rate) => (
                        <option key={rate} value={rate}>
                          ₹{rate}
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              </div>"""
content = content.replace(old_ui, new_ui)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
