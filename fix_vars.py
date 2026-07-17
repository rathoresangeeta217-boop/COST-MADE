import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

dummy_vars = """
  const activeBoard = { name: "Engineered Wood", id: "ew" };

  const calcData = {
    totals: {
      grandTotal: 15000,
      boardsSqFt: 50,
      materialCost: 5000,
      backingCost: 1000,
      hardwareCost: 2000,
      laborCost: 3000,
      packagingCost: 500,
      toolingCost: 500,
      netManufacturingCost: 12000,
      profitMargin: 3000
    },
    pieces: [
      { label: "Top/Bottom", w: width, h: depth, qty: 2, type: "Core", cost: 1000 }
    ],
    hardware: [
      { label: "Screws", qty: 50, cost: 200 }
    ],
    bayWidth: width / (numBays || 1)
  };

  const drawerCalcData = {
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
      { label: "Drawer Front", w: drawerWidth, h: drawerHeight, qty: 1, type: "Core", cost: 500 }
    ],
    hardware: [
      { label: "Channels", qty: 1, cost: 300 }
    ]
  };

  const copySpecifications = () => { alert("Copied"); };
  const copyImagePrompt = () => { alert("Copied"); };
  const exportExcel = () => { alert("Exported"); };
  const exportPDF = () => { alert("Exported"); };

  return (
"""

content = content.replace("  return (", dummy_vars, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
