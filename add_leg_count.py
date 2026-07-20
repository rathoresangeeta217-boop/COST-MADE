import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Update calculateWorkstationCost signature
content = re.sub(
    r'(export function calculateWorkstationCost\(\{.*?legId,\n)',
    r'\1  legCountOverride = 0,\n',
    content,
    flags=re.DOTALL
)

# 2. Update legFrames calculation
content = re.sub(
    r'(const legFrames = )cols \+ 1; // Number of vertical supports',
    r'\1legCountOverride && legCountOverride > 0 ? legCountOverride : cols + 1; // Number of vertical supports',
    content
)

# 3. Add state
content = re.sub(
    r'(const \[legId, setLegId\] = useState<string>\("board"\);)',
    r'\1\n  const [legCountOverride, setLegCountOverride] = useState<number>(0); // 0 means default',
    content
)

# 4. Add to useEffect state hydration
content = re.sub(
    r'(if \(c\.legId !== undefined\) setLegId\(c\.legId\);)',
    r'\1\n        if (c.legCountOverride !== undefined) setLegCountOverride(c.legCountOverride);',
    content
)

# 5. Add to save/update config
content = re.sub(
    r'(legId,\n)(      boardLegType,)',
    r'\1      legCountOverride,\n\2',
    content
)
content = re.sub(
    r'(legId,\n)(    boardLegType,)',
    r'\1    legCountOverride,\n\2',
    content
)

# 6. Add UI for legCountOverride
ui_insert = """              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Custom Leg Count
                  </label>
                  <input
                    type="number"
                    value={legCountOverride === 0 ? '' : legCountOverride}
                    onChange={(e) => setLegCountOverride(Number(e.target.value) || 0)}
                    placeholder="Auto"
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                    min="0"
                  />
                  <p className="text-xs text-gray-500 mt-1">Leave blank for auto-calculation based on layout.</p>
                </div>"""

content = content.replace(
    '                )}',
    '                )}\n' + ui_insert,
    1 # Only the first occurrence which is around line 1604, wait, let's be more specific.
)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
