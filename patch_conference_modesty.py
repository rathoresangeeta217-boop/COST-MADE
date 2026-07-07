import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Add state variables
state_vars = """  const [wireManagement, setWireManagement] = useState<string>("none");
  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);
  const [includeModesty, setIncludeModesty] = useState<boolean>(true);
  const [modestyType, setModestyType] = useState<string>("standard");"""
content = re.sub(r'  const \[wireManagement, setWireManagement\] = useState<string>\("none"\);\n  const \[addLeatherlite, setAddLeatherlite\] = useState<boolean>\(false\);\n  const \[copiedPrompt, setCopiedPrompt\] = useState<boolean>\(false\);', state_vars, content)

# 2. Update calculation
old_modesty_calc = """  // Modesty Panel (default one central modesty for stability)
  const modestyAreaSqMm = (mainWidth - 200) * 400; // 400mm high modesty
  const modestyAreaSqFt = modestyAreaSqMm / 90000;
  const modestyCost = modestyAreaSqFt * board.costPerSqFt;
  bDetails.push({
      label: `Modesty Panel (${modestyAreaSqFt.toFixed(2)} sq.ft)`,
      cost: Math.round(modestyCost)
  });
  bCostTotal += modestyCost;"""

new_modesty_calc = """  // Modesty Panel
  if (includeModesty) {
      const modestyHeight = modestyType === "full" ? 715 : 400;
      const modestyAreaSqMm = (mainWidth - 200) * modestyHeight;
      const modestyAreaSqFt = modestyAreaSqMm / 90000;
      const modestyCost = modestyAreaSqFt * board.costPerSqFt;
      bDetails.push({
          label: `Modesty Panel (${modestyHeight}mm) (${modestyAreaSqFt.toFixed(2)} sq.ft)`,
          cost: Math.round(modestyCost)
      });
      bCostTotal += modestyCost;
  }"""
content = content.replace(old_modesty_calc, new_modesty_calc)

# 3. Add to UI
ui_section = """            {/* Modesty Panel */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-indigo-500" />
                Modesty Panel
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <label className="flex items-center gap-3 p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="checkbox"
                    checked={includeModesty}
                    onChange={(e) => setIncludeModesty(e.target.checked)}
                    className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                  />
                  <div className="flex flex-col">
                    <span className="font-medium text-gray-900">Include Modesty Panel</span>
                    <span className="text-sm text-gray-500">Add central stability board</span>
                  </div>
                </label>
                {includeModesty && (
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">Modesty Type</label>
                    <select
                      value={modestyType}
                      onChange={(e) => setModestyType(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                    >
                      <option value="standard">Standard (400mm)</option>
                      <option value="full">Full Height (715mm)</option>
                    </select>
                  </div>
                )}
              </div>
            </section>

            {/* Wire Management */}"""
content = content.replace("            {/* Wire Management */}", ui_section)

# 4. Update Exports
content = content.replace('["Leg Type", legType.replace("_", " ").toUpperCase()],', '["Leg Type", legType.replace("_", " ").toUpperCase()],\n        ["Modesty Panel", includeModesty ? (modestyType === "full" ? "Full Height (715mm)" : "Standard (400mm)") : "None"],')

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
