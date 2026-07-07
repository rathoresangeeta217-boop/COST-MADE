import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

modesty_ui = """            {/* Modesty Panel */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileBox className="w-5 h-5 text-indigo-500" />
                Modesty Panel
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex flex-col gap-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl bg-gray-50/50">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-indigo-100 rounded-lg">
                        <LayoutGrid className="w-5 h-5 text-indigo-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">Include Modesty</p>
                        <p className="text-xs text-gray-500">Front privacy panel</p>
                      </div>
                    </div>
                    <input 
                      type="checkbox" 
                      checked={includeModesty} 
                      onChange={(e) => setIncludeModesty(e.target.checked)}
                      className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer"
                    />
                  </div>
                </div>

                {includeModesty && (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">Size / Height</label>
                      <select
                        value={modestyType}
                        onChange={(e) => setModestyType(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                      >
                        <option value="standard">Standard (715mm)</option>
                        <option value="short">Short (600mm)</option>
                        <option value="shorter">Shorter (300mm)</option>
                        <option value="custom">Custom Size</option>
                      </select>
                    </div>

                    {modestyType === "custom" && (
                      <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
                        <label className="block text-sm font-medium text-gray-700">Custom Height (mm)</label>
                        <input
                          type="number"
                          value={customModestyHeight}
                          onChange={(e) => setCustomModestyHeight(Number(e.target.value))}
                          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
                          min="100"
                          max={height - 25}
                        />
                      </div>
                    )}

                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">Finish</label>
                      <select
                        value={modestyFinish}
                        onChange={(e) => setModestyFinish(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                      >
                        <option value="plain">Plain</option>
                        <option value="fluted">Fluted</option>
                      </select>
                    </div>
                  </div>
                )}
              </div>
            </section>

"""

content = content.replace("                        {/* Wire Management */}", modesty_ui + "            {/* Wire Management */}")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
