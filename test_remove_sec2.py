import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Remove section 2 completely
content = re.sub(
    r'\{\/\* Section 2:.*?\{\/\* Section 3:',
    '{/* Section 3:',
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
