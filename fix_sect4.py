import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# I will just find `)}` that are orphaned.
content = re.sub(
    r'            \)\}\n          <\/div>\n\n          \{\/\* Section 3: Detailed Cutting piece specifications list',
    r'          </div>\n\n          {/* Section 3: Detailed Cutting piece specifications list',
    content
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
