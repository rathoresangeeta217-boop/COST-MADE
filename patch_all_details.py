import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Drawer UI
drawer_ui_target = """              <div className="space-y-4 text-sm flex-1">
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" /> Backing PLPB Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.backingCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Channels:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.hardwareCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Assembly Labor:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.laborCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Factory Overheads:</span>
                  <span className="font-mono font-medium">Rs {(drawerCalcData.totals.packagingCost + drawerCalcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                  
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {drawerCalcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {drawerCalcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {drawerCalcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>

              {/* Hardware list breakdown card */}
              <div className="mt-6 border-t border-slate-700 pt-4">
                <h3 className="text-xs font-semibold uppercase text-slate-400 mb-3 tracking-wider">Hardware Breakdown</h3>
                <div className="space-y-2">
                  {drawerCalcData.hardware.map((h, i) => (
                    <div key={i} className="flex justify-between text-xs items-center">
                      <span className="text-slate-300 font-sans">{h.qty}x {h.label}</span>
                      <span className="font-mono text-slate-400">Rs {h.cost.toFixed(0)}</span>
                    </div>
                  ))}
                </div>
              </div>"""

drawer_ui_replace = """              <div className="space-y-6 text-sm flex-1">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                    <span className="font-mono font-medium">Rs {drawerCalcData.totals.materialCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {drawerCalcData.pieces.map((p, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {p.qty}x {p.label} <span className="opacity-70">({(p.totalSqFt || 0).toFixed(1)} sq.ft)</span></span>
                         <span>Rs {p.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" /> Backing PLPB Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.backingCost.toFixed(2)}</span>
                </div>

                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Channels:</span>
                    <span className="font-mono font-medium">Rs {drawerCalcData.totals.hardwareCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {drawerCalcData.hardware.map((h, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {h.qty}x {h.label}</span>
                         <span>Rs {h.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Assembly Labor:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.laborCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Factory Overheads:</span>
                  <span className="font-mono font-medium">Rs {(drawerCalcData.totals.packagingCost + drawerCalcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                  
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {drawerCalcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {drawerCalcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {drawerCalcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>"""
content = content.replace(drawer_ui_target, drawer_ui_replace)

# Now, Storage UI
storage_ui_target = """              <div className="space-y-4 text-sm">
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" /> Backing PLPB Cost:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.backingCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Locks:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.hardwareCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Assembly Labor:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.laborCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Factory Overheads:</span>
                  <span className="font-mono font-medium">Rs {(calcData.totals.packagingCost + calcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                  
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {calcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {calcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {calcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>"""

storage_ui_replace = """              <div className="space-y-6 text-sm">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                    <span className="font-mono font-medium">Rs {calcData.totals.materialCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {calcData.pieces.map((p, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {p.qty}x {p.label} <span className="opacity-70">({(p.totalSqFt || 0).toFixed(1)} sq.ft)</span></span>
                         <span>Rs {p.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" /> Backing PLPB Cost:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.backingCost.toFixed(2)}</span>
                </div>

                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Locks:</span>
                    <span className="font-mono font-medium">Rs {calcData.totals.hardwareCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {calcData.hardware.map((h, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {h.qty}x {h.label}</span>
                         <span>Rs {h.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Assembly Labor:</span>
                  <span className="font-mono font-medium">Rs {calcData.totals.laborCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Factory Overheads:</span>
                  <span className="font-mono font-medium">Rs {(calcData.totals.packagingCost + calcData.totals.toolingCost).toFixed(2)}</span>
                </div>
                  
                <div className="my-4 border-t border-slate-700/60 pt-4" />

                <div className="flex justify-between font-bold text-slate-100">
                  <span>Manufacturing Cost:</span>
                  <span className="font-mono">Rs {calcData.totals.netManufacturingCost.toFixed(2)}</span>
                </div>

                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Profit Margin (25%):</span>
                  <span>Rs {calcData.totals.profitMargin.toFixed(2)}</span>
                </div>

                <div className="border-t-2 border-dashed border-slate-800 my-2.5 pt-4 flex justify-between items-baseline">
                  <span className="font-bold text-base text-slate-200">TOTAL PRICE:</span>
                  <span className="font-mono text-2xl font-bold text-indigo-400">
                    Rs {calcData.totals.grandTotal.toFixed(0)}
                  </span>
                </div>
              </div>"""

content = content.replace(storage_ui_target, storage_ui_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
