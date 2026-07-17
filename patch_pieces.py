import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Update lockerCalcData pieces
pieces_target = """      pieces: [
        { label: "Locker Door", l: computedLockerWidth / lockerColumns, w: computedLockerWidth / lockerColumns, h: computedLockerHeight / lockerTiers, qty: locksQty, type: "Metal", cost: doorsSqFt * metalRate, totalSqFt: doorsSqFt, rate: metalRate }
      ],"""
pieces_replace = """      pieces: [
        { label: "Back Panel", l: computedLockerHeight, w: computedLockerWidth, h: 0, qty: 1, type: "Metal", cost: backSqFt * metalRate, totalSqFt: backSqFt, rate: metalRate },
        { label: "Side Panels", l: computedLockerHeight, w: lockerDepth, h: 0, qty: 2, type: "Metal", cost: sidesSqFt * metalRate, totalSqFt: sidesSqFt, rate: metalRate },
        { label: "Top & Bottom", l: computedLockerWidth, w: lockerDepth, h: 0, qty: 2, type: "Metal", cost: tbSqFt * metalRate, totalSqFt: tbSqFt, rate: metalRate },
        ...(lockerColumns > 1 ? [{ label: "Vertical Partitions", l: computedLockerHeight, w: lockerDepth, h: 0, qty: lockerColumns - 1, type: "Metal", cost: verticalDivSqFt * metalRate, totalSqFt: verticalDivSqFt, rate: metalRate }] : []),
        ...(lockerTiers > 1 ? [{ label: "Horizontal Shelves", l: computedLockerWidth / lockerColumns, w: lockerDepth, h: 0, qty: lockerColumns * (lockerTiers - 1), type: "Metal", cost: horizontalShelvesSqFt * metalRate, totalSqFt: horizontalShelvesSqFt, rate: metalRate }] : []),
        { label: "Locker Doors", l: computedLockerHeight / lockerTiers, w: computedLockerWidth / lockerColumns, h: 0, qty: locksQty, type: "Metal", cost: doorsSqFt * metalRate, totalSqFt: doorsSqFt, rate: metalRate }
      ],"""
content = content.replace(pieces_target, pieces_replace)

# Now, we need to add the UI for the pieces breakdown to the Locker section.
# I will find where Hardware Breakdown is rendered in locker
ui_target = """              {/* Hardware list breakdown card */}
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
              </div>"""

ui_replace = """              {/* Component breakdown card */}
              <div className="mt-6 border-t border-slate-700 pt-4">
                <h3 className="text-xs font-semibold uppercase text-slate-400 mb-3 tracking-wider">Component Breakdown (Sheet Metal)</h3>
                <div className="space-y-3">
                  {lockerCalcData.pieces.map((p, i) => (
                    <div key={i} className="flex flex-col gap-1 text-xs">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-200 font-sans font-medium">{p.qty}x {p.label}</span>
                        <span className="font-mono text-slate-300 font-bold">Rs {p.cost.toFixed(0)}</span>
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-slate-500 font-mono">
                        <span>{Math.round(p.l)} × {Math.round(p.w)} mm</span>
                        <span>{p.totalSqFt.toFixed(1)} sq.ft @ Rs {p.rate}/sq.ft</span>
                      </div>
                    </div>
                  ))}
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
              </div>"""

content = content.replace(ui_target, ui_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
