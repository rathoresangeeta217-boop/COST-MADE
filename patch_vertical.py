import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. ColumnConfig style
content = content.replace(
    'style: "open" | "shutter_solid" | "shutter_glass" | "shutters_double" | "3_drawers" | "2_drawers" | "1_drawer" | "1_drawer_open" | "1_drawer_1_shutter";',
    'style: "open" | "shutter_solid" | "shutter_glass" | "shutters_double" | "3_drawers" | "2_drawers" | "1_drawer" | "1_drawer_open" | "1_drawer_1_shutter" | "vertical_horizontal";'
)

# 2. Descriptions in two places
content = content.replace(
    'else if (bay.style === "1_drawer_1_shutter") desc = `1 Drawer at top (lock: ${bay.lock}), solid shutter below (lock: ${bay.shutterLock || \'none\'})`;',
    'else if (bay.style === "1_drawer_1_shutter") desc = `1 Drawer at top (lock: ${bay.lock}), solid shutter below (lock: ${bay.shutterLock || \'none\'})`;\n      else if (bay.style === "vertical_horizontal") desc = `Vertical bay with ${bay.shelves} horizontal shelves on one side`;'
)

content = content.replace(
    'else if (bay.style === "1_drawer_1_shutter") desc = `1 utility drawer at top (lock: ${bay.lock}), single wood door shutter below (lock: ${bay.shutterLock || \'none\'}).`;',
    'else if (bay.style === "1_drawer_1_shutter") desc = `1 utility drawer at top (lock: ${bay.lock}), single wood door shutter below (lock: ${bay.shutterLock || \'none\'}).`;\n      else if (bay.style === "vertical_horizontal") desc = `Vertical bay with ${bay.shelves} horizontal shelves on one side.`;'
)

# 3. Dropdown option
content = content.replace(
    '<option value="1_drawer_1_shutter">1 drawer at top + Solid Shutter</option>',
    '<option value="1_drawer_1_shutter">1 drawer at top + Solid Shutter</option>\n                        <option value="vertical_horizontal">Vertical Bay with Horizontal</option>'
)

# 4. totalHalfShelvesCount variable
content = content.replace(
    'let totalVerticalShelvesCount = 0;',
    'let totalVerticalShelvesCount = 0;\n    let totalHalfShelvesCount = 0;'
)

# 5. Shelves logic
shelves_logic_old = """      if (bay.shelves > 0) {
        totalShelvesCount += bay.shelves - (removedH / cols);
      }
      if (bay.verticalShelves && bay.verticalShelves > 0) {
        totalVerticalShelvesCount += bay.verticalShelves - (removedV / rows);
      }"""
shelves_logic_new = """      if (bay.style === "vertical_horizontal") {
        totalVerticalShelvesCount += 1;
        if (bay.shelves > 0) {
          totalHalfShelvesCount += bay.shelves;
        }
      } else {
        if (bay.shelves > 0) {
          totalShelvesCount += bay.shelves - (removedH / cols);
        }
        if (bay.verticalShelves && bay.verticalShelves > 0) {
          totalVerticalShelvesCount += bay.verticalShelves - (removedV / rows);
        }
      }"""
content = content.replace(shelves_logic_old, shelves_logic_new)

# 6. Adding the half shelves to pieces
half_shelves_logic = """    if (totalHalfShelvesCount > 0) {
      const halfShelfW = (bayWidth / 2) - 2;
      pieces.push({
        label: "Internal Adjustable Shelves (Half Width)",
        w: halfShelfW,
        l: depth - 20,
        qty: totalHalfShelvesCount,
        ebMm: halfShelfW * totalHalfShelvesCount,
      });
    }"""
content = content.replace(
    'if (totalVerticalShelvesCount > 0) {',
    half_shelves_logic + '\n\n    if (totalVerticalShelvesCount > 0) {'
)

# 7. Render SVG for vertical_horizontal
svg_render = """                            {bay.style === "1_drawer_open" && ("""
new_svg_render = """                            {bay.style === "vertical_horizontal" && (
                              <g>
                                <line x1={bayX + bayW / 2} y1={bayY} x2={bayX + bayW / 2} y2={bayY + bayH} stroke="#334155" strokeWidth="2.5" />
                                {Array.from({ length: bay.shelves || 0 }).map((_, sIdx) => {
                                  const sY = bayY + ((sIdx + 1) * bayH) / ((bay.shelves || 0) + 1);
                                  return (
                                    <line key={`h-${sIdx}`} x1={bayX + bayW / 2} y1={sY} x2={bayX + bayW - 2} y2={sY} stroke="#334155" strokeWidth="2" />
                                  );
                                })}
                              </g>
                            )}

                            {bay.style === "1_drawer_open" && ("""
content = content.replace(svg_render, new_svg_render)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Patched!")
