import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# Update signature
content = content.replace("  addLeatherlite,\n}: any) {", "  addLeatherlite,\n  legCountInput,\n}: any) {")

# Replace legCount definition
content = content.replace("  let legCount = mainWidth >= 2400 ? 3 : 2;", "  let legCount = legCountInput || (mainWidth >= 2400 ? 3 : 2);")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
