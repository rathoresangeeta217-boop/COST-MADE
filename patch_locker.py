import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = r'<div className="space-y-4 text-sm flex-1">\s*<div className="flex justify-between items-center text-slate-300">\s*<span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Sheet Metal Cost:</span>\s*<span className="font-mono font-medium">Rs \{lockerCalcData\.totals\.materialCost\.toFixed\(2\)\}</span>\s*</div>(.*?)</div>\s*</div>\s*\{/\* Component breakdown card \*/\}'

replacement = """              <div className="space-y-6 text-sm flex-1">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Sheet Metal Cost:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.materialCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {lockerCalcData.pieces.map((p, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {p.qty}x {p.label} <span className="opacity-70">({(p.totalSqFt || 0).toFixed(1)} sq.ft)</span></span>
                         <span>Rs {p.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-rose-400" /> Hardware & Locks:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.hardwareCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1">
                    {lockerCalcData.hardware.map((h, i) => (
                       <div key={i} className="flex justify-between items-center text-[11px] text-slate-500 font-mono">
                         <span>- {h.qty}x {h.label}</span>
                         <span>Rs {h.cost.toFixed(0)}</span>
                       </div>
                    ))}
                  </div>
                </div>
                
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center text-slate-300">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Bending & Assembly:</span>
                    <span className="font-mono font-medium">Rs {lockerCalcData.totals.laborCost.toFixed(2)}</span>
                  </div>
                  <div className="pl-6 flex flex-col gap-1 text-[11px] text-slate-500 font-mono">
                     <div className="flex justify-between items-center">
                       <span>- Base Fabrication ({lockerCalcData.totals.totalSqFt?.toFixed(1) || '0'} sq.ft)</span>
                       <span>Rs {(lockerCalcData.totals.baseLabor || 0).toFixed(0)}</span>
                     </div>
                     {(lockerCalcData.totals.cncCost || 0) > 0 && (
                       <div className="flex justify-between items-center">
                         <span>- CNC Punching / Louvers</span>
                         <span>Rs {lockerCalcData.totals.cncCost.toFixed(0)}</span>
                       </div>
                     )}
                  </div>
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

              {/* Component breakdown card */}"""

content = re.sub(target, replacement, content, flags=re.DOTALL)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
