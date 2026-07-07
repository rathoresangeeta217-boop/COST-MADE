import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("const [wireManagement,\n    flapBoxRate, setWireManagement]", "const [wireManagement, setWireManagement]")
content = content.replace("const [wireManagement,\nflapBoxRate, setWireManagement]", "const [wireManagement, setWireManagement]")

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
