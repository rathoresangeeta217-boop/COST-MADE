import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """      )}
    </div>
  );
}"""

replacement = """      )}

      {activeTab === "locker" && (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          {/* Left Side: Parameters */}
          <div className="xl:col-span-7 space-y-6">
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Locker Dimensions
                  </h2>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Width (W) mm</label>
                  <input
                    type="number"
                    value={lockerWidth}
                    onChange={(e) => setLockerWidth(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Height (H) mm</label>
                  <input
                    type="number"
                    value={lockerHeight}
                    onChange={(e) => setLockerHeight(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Depth (D) mm</label>
                  <input
                    type="number"
                    value={lockerDepth}
                    onChange={(e) => setLockerDepth(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Columns (Bays)</label>
                  <input
                    type="number"
                    min={1} max={10}
                    value={lockerColumns}
                    onChange={(e) => setLockerColumns(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Tiers (Doors per Column)</label>
                  <input
                    type="number"
                    min={1} max={12}
                    value={lockerTiers}
                    onChange={(e) => setLockerTiers(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  />
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Material Configuration
                  </h2>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Thickness (CRCA Sheet)</label>
                  <select
                    value={lockerThickness}
                    onChange={(e) => setLockerThickness(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-mono"
                  >
                    <option value={0.6}>0.6 mm</option>
                    <option value={0.8}>0.8 mm</option>
                    <option value={1.0}>1.0 mm</option>
                    <option value={1.2}>1.2 mm</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side */}
          <div className="xl:col-span-5 space-y-6">
            {/* Live Drawer Blueprint */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Locker Blueprint
                  </h2>
                </div>
              </div>
              <div className="flex justify-center p-6 bg-slate-50 relative border border-gray-200 rounded-xl overflow-hidden">
                <svg
                  viewBox={`-50 -50 ${lockerWidth + 100} ${lockerHeight + 100}`}
                  width={(lockerWidth + 100) * 0.4}
                  height={(lockerHeight + 100) * 0.4}
                  className="drop-shadow-2xl transition-all duration-200 max-h-[600px] w-auto"
                  xmlns="http://www.w3.org/2000/svg"
                >
                   {/* Main Frame */}
                   <rect x="0" y="0" width={lockerWidth} height={lockerHeight} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" rx="4" />
                   
                   {/* Columns */}
                   {Array.from({ length: lockerColumns }).map((_, cIdx) => {
                     const colWidth = lockerWidth / lockerColumns;
                     const colX = cIdx * colWidth;
                     return (
                       <g key={`col-${cIdx}`}>
                         {/* Vertical Divider */}
                         {cIdx > 0 && <line x1={colX} y1="0" x2={colX} y2={lockerHeight} stroke="#94a3b8" strokeWidth="4" />}
                         
                         {/* Doors (Tiers) */}
                         {Array.from({ length: lockerTiers }).map((_, tIdx) => {
                           const tierHeight = lockerHeight / lockerTiers;
                           const tierY = tIdx * tierHeight;
                           const pad = 4;
                           return (
                             <g key={`door-${cIdx}-${tIdx}`}>
                               <rect 
                                 x={colX + pad} 
                                 y={tierY + pad} 
                                 width={colWidth - pad*2} 
                                 height={tierHeight - pad*2} 
                                 fill="#cbd5e1" 
                                 stroke="#94a3b8" 
                                 strokeWidth="2" 
                                 rx="2"
                               />
                               {/* Louvers / Vents */}
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />

                               {/* Lock / Handle */}
                               <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                               <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2" fill="#475569" />
                             </g>
                           )
                         })}
                       </g>
                     )
                   })}
                   
                   {/* Dimension labels */}
                   <text x={lockerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(16, lockerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{lockerWidth}mm</text>
                   <text x="-20" y={lockerHeight / 2} fill="#64748b" fontSize={Math.max(16, lockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${lockerHeight/2})`}>{lockerHeight}mm</text>
                </svg>
              </div>
            </div>

            <div className="bg-slate-900 rounded-2xl shadow-xl p-6 text-white border border-slate-800 flex flex-col h-full">
              <div className="flex items-center gap-3 mb-6 border-b border-slate-700 pb-4">
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
                  <IndianRupee className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white tracking-tight">Locker Cost</h2>
                  <p className="text-xs text-slate-400 font-mono">Net Valuation</p>
                </div>
              </div>

              <div className="space-y-4 text-sm flex-1">
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Sheet Metal Cost:</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Locks:</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.hardwareCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Bending & Assembly:</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.laborCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Powder Coating & Finish:</span>
                  <span className="font-mono font-medium">Rs {(lockerCalcData.totals.packagingCost + lockerCalcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                  
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {lockerCalcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {lockerCalcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {lockerCalcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>

              {/* Hardware list breakdown card */}
              <div className="mt-6 border-t border-slate-700 pt-4">
                <h3 className="text-xs font-semibold uppercase text-slate-400 mb-3 tracking-wider">Hardware Breakdown</h3>
                <div className="space-y-2">
                  {lockerCalcData.hardware.map((h, i) => (
                    <div key={i} className="flex justify-between text-xs items-center">
                      <span className="text-slate-300 font-sans">{h.qty}x {h.label}</span>
                      <span className="font-mono text-slate-400">Rs {h.cost.toFixed(0)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
