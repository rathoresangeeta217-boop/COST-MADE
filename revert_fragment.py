import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "            ) : (\n              <>",
    "            ) : ("
)

content = content.replace(
    "              </>\n            )}\n          </div>\n\n          {/* Section 3:",
    "            )}\n          </div>\n\n          {/* Section 3:"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
