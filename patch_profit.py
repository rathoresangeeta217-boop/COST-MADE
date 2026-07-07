import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """  const makingCharges = LABOR_COST * mainTopSqFt; // labor based on top size
  const totalCostBeforeProfit = totalMaterialCost + makingCharges + PACKING_COST + TOOLING_COST;
  const profit = totalCostBeforeProfit * PROFIT_PERCENTAGE;
  const finalPrice = totalCostBeforeProfit + profit;"""

new_block = """  const makingCharges = LABOR_COST * mainTopSqFt; // labor based on top size
  const totalCostBeforeProfit = totalMaterialCost + makingCharges + PACKING_COST + TOOLING_COST;
  const appliedProfitPercentage = legType === "box_fluted" ? 0.40 : PROFIT_PERCENTAGE;
  const profit = totalCostBeforeProfit * appliedProfitPercentage;
  const finalPrice = totalCostBeforeProfit + profit;"""

content = content.replace(old_block, new_block)

old_block2 = """      ["Packing & Tooling", `Rs. ${(costSummary.packing + costSummary.tooling).toLocaleString()}`],
      ["Profit (25%)", `Rs. ${costSummary.profit.toLocaleString()}`],
    ];"""

new_block2 = """      ["Packing & Tooling", `Rs. ${(costSummary.packing + costSummary.tooling).toLocaleString()}`],
      [`Profit (${legType === "box_fluted" ? "40%" : "25%"})`, `Rs. ${costSummary.profit.toLocaleString()}`],
    ];"""

content = content.replace(old_block2, new_block2)

old_block3 = """    detailsData.push(["Packing", costSummary.packing]);
    detailsData.push(["Tooling", costSummary.tooling]);
    detailsData.push(["Profit (25%)", costSummary.profit]);
    detailsData.push([""]);"""

new_block3 = """    detailsData.push(["Packing", costSummary.packing]);
    detailsData.push(["Tooling", costSummary.tooling]);
    detailsData.push([`Profit (${legType === "box_fluted" ? "40%" : "25%"})`, costSummary.profit]);
    detailsData.push([""]);"""

content = content.replace(old_block3, new_block3)

old_block4 = """                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Profit (25%)</span>
                  <span className="font-medium text-gray-900">₹{costSummary.profit.toLocaleString()}</span>
                </div>"""

new_block4 = """                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">Profit ({legType === "box_fluted" ? "40%" : "25%"})</span>
                  <span className="font-medium text-gray-900">₹{costSummary.profit.toLocaleString()}</span>
                </div>"""

content = content.replace(old_block4, new_block4)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
