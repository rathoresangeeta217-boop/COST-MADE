import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """            {/* Mica/Laminate Options */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Inner Laminate/Mica Finish
                </label>
                <select
                  value={innerMica}
                  onChange={(e) => setInnerMica(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  <option value="none">Raw Finish (No Inner Mica)</option>
                  <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                  <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                  Outer Laminate/Mica Finish
                </label>
                <select
                  value={outerMica}
                  onChange={(e) => setOuterMica(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                >
                  <option value="none">Raw Finish (No Outer Mica)</option>
                  <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                  <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                </select>
              </div>
            </div>"""
            
replace = """            {/* Mica/Laminate Options */}
            {constructionCategory !== "metal" && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Inner Laminate/Mica Finish
                  </label>
                  <select
                    value={innerMica}
                    onChange={(e) => setInnerMica(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                  >
                    <option value="none">Raw Finish (No Inner Mica)</option>
                    <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                    <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">
                    Outer Laminate/Mica Finish
                  </label>
                  <select
                    value={outerMica}
                    onChange={(e) => setOuterMica(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                  >
                    <option value="none">Raw Finish (No Outer Mica)</option>
                    <option value="0.8">0.8 mm Laminate (+Rs 35/sq.ft)</option>
                    <option value="1.0">1.0 mm Laminate (+Rs 56/sq.ft)</option>
                  </select>
                </div>
              </div>
            )}"""

content = content.replace(target, replace)

dna_target = """              <div>• Core Board Wood: {activeBoard.name}</div>
              <div>• Outer Mica overlay: {outerMica === "none" ? "None" : `${outerMica}mm overlay`}</div>"""
dna_replace = """              {constructionCategory !== "metal" && (
                <>
                  <div>• Core Board Wood: {activeBoard.name}</div>
                  <div>• Outer Mica overlay: {outerMica === "none" ? "None" : `${outerMica}mm overlay`}</div>
                </>
              )}"""
content = content.replace(dna_target, dna_replace)              

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
