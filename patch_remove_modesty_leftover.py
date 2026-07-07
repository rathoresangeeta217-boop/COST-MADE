import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("      bCostTotal += modestyCost;\n  }", "")
content = content.replace("      bCostTotal += modestyCost;\n  }\n", "")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
