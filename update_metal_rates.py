import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

metal_rates = """  if (boardId === "crca_powder_coated") {
    switch (thickness) {
      case 2: return 125;
      case 1.6: return 96;
      case 1.2: return 72;
      case 1: return 62;
      case 0.8: return 52;
      case 0.6: return 41;
      default: return baseRate * (thickness / 1.2);
    }
  }
  if (boardId === "ss_304") {
    return baseRate * (thickness / 1.2);
  }"""

content = re.sub(
    r'if \(boardId === "crca_powder_coated" \|\| boardId === "ss_304"\) \{\s*return baseRate \* \(thickness / 1\.2\);\s*\}',
    metal_rates.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
