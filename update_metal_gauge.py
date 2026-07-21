import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Update getAvailableThicknesses
target1 = '  if (boardId === "crca_powder_coated" || boardId === "ss_304") {\n    return [0.8, 1, 1.2, 1.6, 2];\n  }'
replacement1 = '  if (boardId === "crca_powder_coated" || boardId === "ss_304") {\n    return [0.6, 0.8, 1, 1.2, 1.6, 2];\n  }'
content = content.replace(target1, replacement1)

# 2. Add formatThicknessLabel function after getAvailableThicknesses
target2 = 'export const getBoardRate ='
replacement2 = '''export const formatThicknessLabel = (boardId: string, thickness: number): string => {
  if (boardId === "crca_powder_coated" || boardId === "ss_304") {
    switch (thickness) {
      case 2: return "14 Gauge (2.0mm)";
      case 1.6: return "16 Gauge (1.6mm)";
      case 1.2: return "18 Gauge (1.2mm)";
      case 1: return "20 Gauge (1.0mm)";
      case 0.8: return "22 Gauge (0.8mm)";
      case 0.6: return "24 Gauge (0.6mm)";
      default: return `${thickness} mm`;
    }
  }
  return `${thickness} mm`;
};

export const getBoardRate ='''
if 'export const formatThicknessLabel' not in content:
    content = content.replace(target2, replacement2)

def replace_thickness_display(match):
    prefix = match.group(1)
    board_var = match.group(2)
    suffix = match.group(3)
    return f"{prefix}{board_var}{suffix}{{formatThicknessLabel({board_var}, t)}}"

pattern = re.compile(r'(getAvailableThicknesses\(\s*([a-zA-Z0-9_]+)\s*,\s*quality\s*\)\.map\(\(t\)\s*=>\s*\(\s*<option[^>]*>)(?:\s*\{t\}\s*mm)')
content = pattern.sub(lambda m: m.group(1) + f"{{formatThicknessLabel({m.group(2)}, t)}}", content)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
