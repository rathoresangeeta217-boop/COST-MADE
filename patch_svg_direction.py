import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace the bay rendering calculations:
old_svg_calc = """                      {/* Draw column dividers and styles */}
                      {bays.map((bay, idx) => {
                        const bayW = (drawW - 16) / numBays;
                        const bayX = paddingX + 8 + idx * bayW;
                        const bayY = paddingY + 8;
                        const bayH = drawH - 16;

                        return (
                          <g key={idx}>
                            {/* Vertical divider lines between bays */}
                            {idx > 0 && (
                              <line
                                x1={bayX}
                                y1={bayY}
                                x2={bayX}
                                y2={bayY + bayH}
                                stroke="#475569"
                                strokeWidth="2.5"
                              />
                            )}"""

new_svg_calc = """                      {/* Draw column/row dividers and styles */}
                      {bays.map((bay, idx) => {
                        const isHoriz = bayDirection === 'horizontal';
                        const bayW = isHoriz ? (drawW - 16) : (drawW - 16) / numBays;
                        const bayH = isHoriz ? (drawH - 16) / numBays : (drawH - 16);
                        const bayX = paddingX + 8 + (isHoriz ? 0 : idx * bayW);
                        const bayY = paddingY + 8 + (isHoriz ? idx * bayH : 0);

                        return (
                          <g key={idx}>
                            {/* Divider lines between bays */}
                            {idx > 0 && (
                              <line
                                x1={isHoriz ? paddingX + 8 : bayX}
                                y1={isHoriz ? bayY : paddingY + 8}
                                x2={isHoriz ? paddingX + drawW - 8 : bayX}
                                y2={isHoriz ? bayY : paddingY + drawH - 8}
                                stroke="#475569"
                                strokeWidth="2.5"
                              />
                            )}"""

content = content.replace(old_svg_calc, new_svg_calc)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
