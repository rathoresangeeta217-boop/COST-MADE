import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# I need to wrap the wooden Section 2 in a Fragment `<>` and `</>`
# It starts right after `            ) : (`
content = content.replace(
    "            ) : (",
    "            ) : (\n              <>"
)

# And it ends at the `)}` before `          {/* Section 3:`
content = content.replace(
    "            )}\n          </div>\n\n          {/* Section 3:",
    "              </>\n            )}\n          </div>\n\n          {/* Section 3:"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
