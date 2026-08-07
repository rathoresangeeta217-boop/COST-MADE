import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Drawer calcData
old_drawer_labor = """    const laborCost = Math.round((materialCost + hardwareCost) * 0.20);
    const packagingCost = 300;
    const toolingCost = 100;
    const netManufacturing = materialCost + hardwareCost + laborCost + packagingCost + toolingCost;"""
new_drawer_labor = """    const wasteCost = materialCost * 0.15;
    const laborCost = Math.round((materialCost + wasteCost + hardwareCost) * 0.20);
    const packagingCost = 300;
    const toolingCost = 100;
    const netManufacturing = materialCost + wasteCost + hardwareCost + laborCost + packagingCost + toolingCost;"""
content = content.replace(old_drawer_labor, new_drawer_labor)

old_drawer_totals = """      totals: {
        grandTotal: netManufacturing + profit,
        materialCost,
        backingCost: 0,"""
new_drawer_totals = """      totals: {
        grandTotal: netManufacturing + profit,
        materialCost,
        wasteCost,
        backingCost: 0,"""
content = content.replace(old_drawer_totals, new_drawer_totals)

old_drawer_ui = """                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="pl-6 pb-1 space-y-1">"""
new_drawer_ui = """                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material Cost:</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-yellow-400" /> Material Waste (15%):</span>
                  <span className="font-mono font-medium">Rs {drawerCalcData.totals.wasteCost.toFixed(2)}</span>
                </div>
                <div className="pl-6 pb-1 space-y-1">"""
content = content.replace(old_drawer_ui, new_drawer_ui)


# Locker calcData
old_locker_labor = """    const baseLabor = Math.round((materialCost + hardwareCost) * 0.20);
    const cncCost = lockerCncDesign ? (activeDoors * 80) : 0; // 80 rs per door for CNC
    const laborCost = baseLabor + cncCost;
    const packagingCost = 300;
    const toolingCost = 100;
    
    const netManufacturingCost = materialCost + hardwareCost + laborCost + packagingCost + toolingCost;"""
new_locker_labor = """    const wasteCost = materialCost * 0.15;
    const baseLabor = Math.round((materialCost + wasteCost + hardwareCost) * 0.20);
    const cncCost = lockerCncDesign ? (activeDoors * 80) : 0; // 80 rs per door for CNC
    const laborCost = baseLabor + cncCost;
    const packagingCost = 300;
    const toolingCost = 100;
    
    const netManufacturingCost = materialCost + wasteCost + hardwareCost + laborCost + packagingCost + toolingCost;"""
content = content.replace(old_locker_labor, new_locker_labor)

old_locker_totals = """      totals: {
        grandTotal,
        materialCost,
        backingCost: 0,"""
new_locker_totals = """      totals: {
        grandTotal,
        materialCost,
        wasteCost,
        backingCost: 0,"""
content = content.replace(old_locker_totals, new_locker_totals)

old_locker_ui = """                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material:</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="pl-6 pb-1 space-y-1">"""
new_locker_ui = """                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-amber-400" /> Carcass Material:</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.materialCost.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-300">
                  <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-yellow-400" /> Material Waste (15%):</span>
                  <span className="font-mono font-medium">Rs {lockerCalcData.totals.wasteCost.toFixed(2)}</span>
                </div>
                <div className="pl-6 pb-1 space-y-1">"""
content = content.replace(old_locker_ui, new_locker_ui)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
