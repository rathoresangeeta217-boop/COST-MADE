import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """      });
    }
}
    // Cost calculations"""

content = content.replace("      });\n    }\n\n    // Cost calculations", replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
