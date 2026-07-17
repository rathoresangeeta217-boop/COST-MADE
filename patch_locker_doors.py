import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Add state
state_target = """  const [lockerBoxHeight, setLockerBoxHeight] = useState<number>(300);"""
state_replace = """  const [lockerBoxHeight, setLockerBoxHeight] = useState<number>(300);
  const [removedLockerDoors, setRemovedLockerDoors] = useState<string[]>([]);
  
  useEffect(() => {
    setRemovedLockerDoors([]);
  }, [lockerColumns, lockerTiers]);"""

content = content.replace(state_target, state_replace, 1)

# 2. Update logic
calc_target = """    const doorsSqFt = lockerColumns * lockerTiers * (wFt / lockerColumns) * (hFt / lockerTiers);
    
    const totalSqFt = backSqFt + sidesSqFt + tbSqFt + verticalDivSqFt + horizontalShelvesSqFt + doorsSqFt;
    
    // Cost
    const metalRate = quality === "affordable" ? 150 : 220; // Default powder coated CRCA metal
    const materialCost = totalSqFt * metalRate;
    
    // Hardware
    const locksQty = lockerColumns * lockerTiers;
    const lockPrice = 120;
    const hingesQty = lockerColumns * lockerTiers * 2;"""

calc_replace = """    const activeDoors = Math.max(0, (lockerColumns * lockerTiers) - removedLockerDoors.length);
    const doorsSqFt = activeDoors * (wFt / lockerColumns) * (hFt / lockerTiers);
    
    const totalSqFt = backSqFt + sidesSqFt + tbSqFt + verticalDivSqFt + horizontalShelvesSqFt + doorsSqFt;
    
    // Cost
    const metalRate = quality === "affordable" ? 150 : 220; // Default powder coated CRCA metal
    const materialCost = totalSqFt * metalRate;
    
    // Hardware
    const locksQty = activeDoors;
    const lockPrice = 120;
    const hingesQty = activeDoors * 2;"""

content = content.replace(calc_target, calc_replace, 1)

calc_dep_target = """  }, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality]);"""
calc_dep_replace = """  }, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors]);"""
content = content.replace(calc_dep_target, calc_dep_replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

