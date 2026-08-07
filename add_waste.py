import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Add wasteCost to calcData.totals
old_calc_totals = """      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: boardsSqFt,
        materialCost: materialCost,
        backingCost: 0,
        hardwareCost: hwCost,
        laborCost,
        packagingCost,
        toolingCost,"""
new_calc_totals = """      totals: {
        grandTotal: netManufacturing + profit,
        boardsSqFt: boardsSqFt,
        materialCost: materialCost,
        wasteCost: materialCost * 0.15,
        backingCost: 0,
        hardwareCost: hwCost,
        laborCost,
        packagingCost,
        toolingCost,"""
content = content.replace(old_calc_totals, new_calc_totals)

old_net_calc = """    const netManufacturing = materialCost + hwCost + laborCost + packagingCost + toolingCost;"""
new_net_calc = """    const wasteCost = materialCost * 0.15;
    const netManufacturing = materialCost + wasteCost + hwCost + laborCost + packagingCost + toolingCost;"""
content = content.replace(old_net_calc, new_net_calc)

old_labor_calc = """    const laborCost = Math.round((materialCost + hwCost) * 0.20);"""
new_labor_calc = """    const laborCost = Math.round((materialCost + (materialCost * 0.15) + hwCost) * 0.20);"""
content = content.replace(old_labor_calc, new_labor_calc)


# Add UI for waste cost
old_ui = """              <div className="flex justify-between text-slate-400 font-mono">
                <span>Carcass Board Material:</span>
                <span>Rs {calcData.totals.materialCost.toFixed(2)}</span>
              </div>
              <div className="pl-4 pb-1 space-y-1">"""
new_ui = """              <div className="flex justify-between text-slate-400 font-mono">
                <span>Carcass Board Material:</span>
                <span>Rs {calcData.totals.materialCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400 font-mono">
                <span>Material Waste (15%):</span>
                <span>Rs {calcData.totals.wasteCost.toFixed(2)}</span>
              </div>
              <div className="pl-4 pb-1 space-y-1">"""
content = content.replace(old_ui, new_ui)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
