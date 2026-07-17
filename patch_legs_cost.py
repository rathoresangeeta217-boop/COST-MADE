import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Update cost calculation to include legs
cost_target = """    const locksCost = lockerLockType !== "none" ? locksQty * lockPrice : 0;
    const hingesCost = hingesQty * hingePrice;
    const hardwareCost = locksCost + hingesCost;"""
cost_replace = """    const locksCost = lockerLockType !== "none" ? locksQty * lockPrice : 0;
    const hingesCost = hingesQty * hingePrice;
    const legsQty = lockerAddBottomLegs ? (computedLockerWidth >= 1800 ? 6 : 4) : 0;
    const legPrice = 150;
    const legsCost = legsQty * legPrice;
    const hardwareCost = locksCost + hingesCost + legsCost;"""
content = content.replace(cost_target, cost_replace)

# Update hardware array
hw_target = """        ...(lockerLockType !== "none" ? [{ label: lockerLockType === "cam" ? "Cam Locks" : lockerLockType === "digital" ? "Digital Locks" : "Padlock Hasps", qty: locksQty, cost: locksCost, unit: "pcs", unitPrice: lockPrice }] : []),
        { label: "Hinges", qty: hingesQty, cost: hingesCost, unit: "pcs", unitPrice: hingePrice }
      ]
    };
  }, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign]);"""
hw_replace = """        ...(lockerLockType !== "none" ? [{ label: lockerLockType === "cam" ? "Cam Locks" : lockerLockType === "digital" ? "Digital Locks" : "Padlock Hasps", qty: locksQty, cost: locksCost, unit: "pcs", unitPrice: lockPrice }] : []),
        { label: "Hinges", qty: hingesQty, cost: hingesCost, unit: "pcs", unitPrice: hingePrice },
        ...(lockerAddBottomLegs ? [{ label: "150mm Bottom Legs", qty: legsQty, cost: legsCost, unit: "pcs", unitPrice: legPrice }] : [])
      ]
    };
  }, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs]);"""
content = content.replace(hw_target, hw_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

