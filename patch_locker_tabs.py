import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Add "locker" to activeTab
content = content.replace('const [activeTab, setActiveTab] = useState<"storage" | "drawer">("storage");', 'const [activeTab, setActiveTab] = useState<"storage" | "drawer" | "locker">("storage");')

# 2. Add locker states below drawerHeight
state_target = """  const [drawerHeight, setDrawerHeight] = useState<number>(150);"""
state_replace = """  const [drawerHeight, setDrawerHeight] = useState<number>(150);
  const [lockerWidth, setLockerWidth] = useState<number>(900);
  const [lockerDepth, setLockerDepth] = useState<number>(450);
  const [lockerHeight, setLockerHeight] = useState<number>(1800);
  const [lockerColumns, setLockerColumns] = useState<number>(3);
  const [lockerTiers, setLockerTiers] = useState<number>(6);
  const [lockerThickness, setLockerThickness] = useState<number>(0.8);"""
content = content.replace(state_target, state_replace, 1)

# 3. Add lockerCalcData below drawerCalcData
calc_target = """  const drawerCalcData = {
    totals: {
      grandTotal: 3000,
      materialCost: 1000,
      backingCost: 200,
      hardwareCost: 500,
      laborCost: 500,
      packagingCost: 100,
      toolingCost: 100,
      netManufacturingCost: 2400,
      profitMargin: 600
    },
    pieces: [
      { label: "Drawer Front", l: drawerWidth, w: drawerWidth, h: drawerHeight, qty: 1, type: "Core", cost: 500, totalSqFt: 5, rate: 100 }
    ],
    hardware: [
      { label: "Channels", qty: 1, cost: 300, unit: "pair", unitPrice: 300 }
    ]
  };"""

calc_replace = calc_target + """
  const lockerCalcData = {
    totals: {
      grandTotal: 12500,
      materialCost: 6000,
      backingCost: 0,
      hardwareCost: 2000,
      laborCost: 1500,
      packagingCost: 500,
      toolingCost: 500,
      netManufacturingCost: 10000,
      profitMargin: 2500
    },
    pieces: [
      { label: "Locker Door", l: lockerWidth / lockerColumns, w: lockerWidth / lockerColumns, h: lockerHeight / lockerTiers, qty: lockerColumns * lockerTiers, type: "Metal", cost: 3000, totalSqFt: 30, rate: 100 }
    ],
    hardware: [
      { label: "Cam Locks", qty: lockerColumns * lockerTiers, cost: 1500, unit: "pcs", unitPrice: 50 },
      { label: "Hinges", qty: lockerColumns * lockerTiers * 2, cost: 500, unit: "pcs", unitPrice: 15 }
    ]
  };"""
content = content.replace(calc_target, calc_replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
