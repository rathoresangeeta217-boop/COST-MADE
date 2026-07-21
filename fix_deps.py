import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_deps = "}, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs]);"
new_deps = "}, [computedLockerWidth, computedLockerHeight, lockerDepth, lockerColumns, lockerTiers, quality, removedLockerDoors, lockerLockType, lockerCncDesign, lockerAddBottomLegs, lockerThickness]);"

content = content.replace(old_deps, new_deps)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
