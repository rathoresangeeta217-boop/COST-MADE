import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """  const appliedProfitPercentage = legType === "box_fluted" ? 0.40 : PROFIT_PERCENTAGE;"""
new_block = """  const appliedProfitPercentage = (legType === "box_fluted" || legType === "round_fluted") ? 0.40 : PROFIT_PERCENTAGE;"""
content = content.replace(old_block, new_block)

old_block2 = """      [`Profit (${legType === "box_fluted" ? "40%" : "25%"})`, `Rs. ${costSummary.profit.toLocaleString()}`],"""
new_block2 = """      [`Profit (${(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})`, `Rs. ${costSummary.profit.toLocaleString()}`],"""
content = content.replace(old_block2, new_block2)

old_block3 = """    detailsData.push([`Profit (${legType === "box_fluted" ? "40%" : "25%"})`, costSummary.profit]);"""
new_block3 = """    detailsData.push([`Profit (${(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})`, costSummary.profit]);"""
content = content.replace(old_block3, new_block3)

old_block4 = """                  <span className="text-gray-600">Profit ({legType === "box_fluted" ? "40%" : "25%"})</span>"""
new_block4 = """                  <span className="text-gray-600">Profit ({(legType === "box_fluted" || legType === "round_fluted") ? "40%" : "25%"})</span>"""
content = content.replace(old_block4, new_block4)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
