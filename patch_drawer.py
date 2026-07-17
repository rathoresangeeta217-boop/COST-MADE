import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Update drawerCalcData
drawer_calc_target = """  const drawerCalcData = {
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
    },"""

drawer_calc_replace = """  const drawerCalcData = {
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
    },"""
# wait, actually it's easier to dynamically compute drawerCalcData instead of hardcoding. Let me check if drawerCalcData is hardcoded.
