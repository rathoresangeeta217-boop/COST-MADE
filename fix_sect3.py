import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "            )}\n          </div>\n\n          {/* Section 3: Detailed Cutting piece specifications list */}",
    "          </div>\n\n          {/* Section 3: Detailed Cutting piece specifications list */}"
)

# And what about line 3621: ')' expected, and 4028: `}` or `}` ?
# Let's see what is near 3621.
