import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace the select box
old_select = """                  <select
                    value={lockerThickness}
                    onChange={(e) => setLockerThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    <option value={0.6}>0.6 mm</option>
                    <option value={0.8}>0.8 mm</option>
                    <option value={1.0}>1.0 mm</option>
                    <option value={1.2}>1.2 mm</option>
                  </select>"""

new_select = """                  <select
                    value={lockerThickness}
                    onChange={(e) => setLockerThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    {[0.6, 0.8, 1, 1.2, 1.6, 2].map((t) => (
                      <option key={t} value={t}>
                        {formatThicknessLabel("crca_powder_coated", t)}
                      </option>
                    ))}
                  </select>"""

content = content.replace(old_select, new_select)

# Replace the metalRate calculation in lockerCalcData
old_rate_calc = """    // Cost
    const metalRate = quality === "affordable" ? 150 : 220; // Default powder coated CRCA metal
    const materialCost = totalSqFt * metalRate;"""

new_rate_calc = """    // Cost
    const baseMetalRate = quality === "affordable" ? 150 : 220; // Default powder coated CRCA metal
    const metalRate = getBoardRate("crca_powder_coated", baseMetalRate, lockerThickness, quality);
    const materialCost = totalSqFt * metalRate;"""

content = content.replace(old_rate_calc, new_rate_calc)

# Need to make sure lockerCalcData includes lockerThickness in useMemo dependencies
old_deps = "}, [lockerWidth, lockerDepth, lockerHeight, lockerColumns, lockerTiers, lockerSizeMode, lockerBoxWidth, lockerBoxHeight, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs, quality]);"
new_deps = "}, [lockerWidth, lockerDepth, lockerHeight, lockerColumns, lockerTiers, lockerSizeMode, lockerBoxWidth, lockerBoxHeight, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs, quality, lockerThickness]);"
content = content.replace(old_deps, new_deps)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
