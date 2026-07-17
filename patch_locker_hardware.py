import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """      hardware: [
        { label: "Cam Locks", qty: locksQty, cost: locksCost, unit: "pcs", unitPrice: lockPrice },
        { label: "Hinges", qty: hingesQty, cost: hingesCost, unit: "pcs", unitPrice: hingePrice }
      ]"""

replace = """      hardware: [
        ...(lockerLockType !== "none" ? [{ label: lockerLockType === "cam" ? "Cam Locks" : lockerLockType === "digital" ? "Digital Locks" : "Padlock Hasps", qty: locksQty, cost: locksCost, unit: "pcs", unitPrice: lockPrice }] : []),
        { label: "Hinges", qty: hingesQty, cost: hingesCost, unit: "pcs", unitPrice: hingePrice }
      ]"""

content = content.replace(target, replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

