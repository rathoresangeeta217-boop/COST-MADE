import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("Aluminum Flap Box (₹{WIRE_MANAGER_COST})", "Aluminum Flap Box (₹{flapBoxRate})")

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
