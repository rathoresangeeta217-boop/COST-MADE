import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Update calculation
calc_target = """    const locksQty = activeDoors;
    const lockPrice = 120;
    const hingesQty = activeDoors * 2;
    const hingePrice = 40;
    
    const locksCost = locksQty * lockPrice;
    const hingesCost = hingesQty * hingePrice;
    const hardwareCost = locksCost + hingesCost;
    
    const laborCost = totalSqFt * 40; // rs per sqft for bending & assembly"""

calc_replace = """    const locksQty = activeDoors;
    let lockPrice = 0;
    if (lockerLockType === "cam") lockPrice = 120;
    else if (lockerLockType === "padlock") lockPrice = 50;
    else if (lockerLockType === "digital") lockPrice = 850;
    
    const hingesQty = activeDoors * 2;
    const hingePrice = 40;
    
    const locksCost = lockerLockType !== "none" ? locksQty * lockPrice : 0;
    const hingesCost = hingesQty * hingePrice;
    const hardwareCost = locksCost + hingesCost;
    
    const baseLabor = totalSqFt * 40;
    const cncCost = lockerCncDesign ? (activeDoors * 80) : 0; // 80 rs per door for CNC
    const laborCost = baseLabor + cncCost;"""

content = content.replace(calc_target, calc_replace, 1)

# 2. Update dependencies
dep_target = "}, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors]);"
dep_replace = "}, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign]);"
content = content.replace(dep_target, dep_replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

