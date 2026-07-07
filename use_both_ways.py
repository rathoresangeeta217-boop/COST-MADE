import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. State
content = content.replace(
    "const [bayDirection, setBayDirection] = useState<'vertical' | 'horizontal'>('vertical');",
    "const [numRows, setNumRows] = useState<number>(1);"
)

# 2. Saving to Project Data
content = content.replace(
    "boardThickness, innerMica, outerMica, numBays, bayDirection, supportLegsCount,",
    "boardThickness, innerMica, outerMica, numBays, numRows, supportLegsCount,"
)

# 3. Loading from Project Data
content = content.replace(
    "if (c.bayDirection) setBayDirection(c.bayDirection);",
    "if (c.numRows) setNumRows(c.numRows);"
)

# 4. Sync bays array size
old_sync = """  // Sync bays array size with numBays
  useEffect(() => {
    if (bays.length < numBays) {
      const added: ColumnConfig[] = Array.from({ length: numBays - bays.length }, () => ({
        style: "open",
        shelves: 1,
        verticalShelves: 0,
        lock: "none",
        handle: true,
        shutterLock: "none",
        shutterHandle: true,
      }));
      setBays([...bays, ...added]);
    } else if (bays.length > numBays) {
      setBays(bays.slice(0, numBays));
    }"""
new_sync = """  // Sync bays array size with numBays * numRows
  useEffect(() => {
    const totalBays = numBays * numRows;
    if (bays.length < totalBays) {
      const added: ColumnConfig[] = Array.from({ length: totalBays - bays.length }, () => ({
        style: "open",
        shelves: 1,
        verticalShelves: 0,
        lock: "none",
        handle: true,
        shutterLock: "none",
        shutterHandle: true,
      }));
      setBays([...bays, ...added]);
    } else if (bays.length > totalBays) {
      setBays(bays.slice(0, totalBays));
    }"""
content = content.replace(old_sync, new_sync)

# 5. useEffect dependencies
content = content.replace(
    "}, [numBays, width]);",
    "}, [numBays, numRows, width]);"
)

# 6. CalcData logic
old_calc_block = """    // Dividers / Vertical Partitions
    const isHoriz = bayDirection === 'horizontal';
    const numPartitions = numBays - 1;
    if (numPartitions > 0) {
      pieces.push({
        label: isHoriz ? "Horizontal Partitions" : "Vertical Partitions",
        w: depth - 20,
        l: isHoriz ? (width - thickness * 2) : sideH,
        qty: numPartitions,
        ebMm: (isHoriz ? (width - thickness * 2) : sideH) * numPartitions,
      });
    }

    // Inside dimensions for columns
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    const baySideH = isHoriz ? Math.max(0, (sideH - totalPartitionThickness) / numBays) : sideH;
    const bayWidth = isHoriz ? innerWidth : Math.max(0, (innerWidth - totalPartitionThickness) / numBays);"""

new_calc_block = """    // Vertical Partitions
    const numPartitions = numBays - 1;
    if (numPartitions > 0) {
      pieces.push({
        label: "Vertical Partitions",
        w: depth - 20,
        l: sideH,
        qty: numPartitions,
        ebMm: sideH * numPartitions,
      });
    }

    // Inside dimensions for columns
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    const bayWidth = Math.max(0, (innerWidth - totalPartitionThickness) / numBays);

    // Horizontal Partitions
    const numHPartitions = numRows - 1;
    if (numHPartitions > 0) {
      pieces.push({
        label: "Horizontal Partitions",
        w: bayWidth,
        l: depth - 20,
        qty: numHPartitions * numBays,
        ebMm: bayWidth * numHPartitions * numBays,
      });
    }
    const totalHPartitionThickness = numHPartitions * thickness;
    const baySideH = Math.max(0, (sideH - totalHPartitionThickness) / numRows);"""
content = content.replace(old_calc_block, new_calc_block)

# 7. UseEffect calcData dependency
content = content.replace(
    "boardThickness, drawerWidth, drawerDepth, drawerHeight, drawerLock, drawerHandle, quality, numBays, supportLegsCount, bays, showAdvancedMaterials, pieceOverrides, thicknessOverrides, innerMica, outerMica, bayDirection]);",
    "boardThickness, drawerWidth, drawerDepth, drawerHeight, drawerLock, drawerHandle, quality, numBays, numRows, supportLegsCount, bays, showAdvancedMaterials, pieceOverrides, thicknessOverrides, innerMica, outerMica]);"
)

# 8. UseEffect drawerCalcData dependency
content = content.replace(
    "[isCustomSize, width, depth, height, boardId, shutterBoardId, backPanelBoardId, drawerBoxBoardId, boardThickness, drawerWidth, drawerDepth, drawerHeight, quality, numBays, supportLegsCount, bays, bayDirection]"
    ,
    "[isCustomSize, width, depth, height, boardId, shutterBoardId, backPanelBoardId, drawerBoxBoardId, boardThickness, drawerWidth, drawerDepth, drawerHeight, quality, numBays, numRows, supportLegsCount, bays]"
)

# 9. UI Header
old_ui_header = """            <div className="flex flex-wrap items-center justify-between border-b border-gray-100 pb-3 gap-4">
              <div className="flex items-center gap-2">
                <LayoutGrid className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  2. Bays & Front configuration
                </h2>
              </div>
              <div className="flex items-center gap-4">
                {/* Orientation Toggle */}
                <div className="flex bg-gray-100 p-1 rounded-lg">
                  <button 
                    onClick={() => setBayDirection('vertical')} 
                    className={`px-3 py-1 rounded-md text-xs font-semibold ${bayDirection === 'vertical' ? 'bg-white shadow text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                  >
                    Vertical
                  </button>
                  <button 
                    onClick={() => setBayDirection('horizontal')} 
                    className={`px-3 py-1 rounded-md text-xs font-semibold ${bayDirection === 'horizontal' ? 'bg-white shadow text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                  >
                    Horizontal
                  </button>
                </div>
                {/* Bays Counter */}
                <div className="flex items-center gap-2.5">
                  <button
                    type="button"
                    onClick={() => setNumBays(Math.max(1, numBays - 1))}
                    disabled={numBays <= 1}
                    className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 disabled:opacity-40 transition-colors"
                  >
                    <Minus className="w-4 h-4" />
                  </button>
                  <span className="font-bold text-gray-900 text-sm font-mono w-16 text-center">{numBays} Bays</span>
                  <button
                    type="button"
                    onClick={() => setNumBays(numBays + 1)}
                    className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>"""

new_ui_header = """            <div className="flex flex-wrap items-center justify-between border-b border-gray-100 pb-3 gap-4">
              <div className="flex items-center gap-2">
                <LayoutGrid className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  2. Bays & Front configuration
                </h2>
              </div>
              <div className="flex items-center gap-4">
                {/* Grid Controls */}
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2.5">
                    <button
                      type="button"
                      onClick={() => setNumBays(Math.max(1, numBays - 1))}
                      disabled={numBays <= 1}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 disabled:opacity-40 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="font-bold text-gray-900 text-sm font-mono w-24 text-center">{numBays} Columns</span>
                    <button
                      type="button"
                      onClick={() => setNumBays(numBays + 1)}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="flex items-center gap-2.5">
                    <button
                      type="button"
                      onClick={() => setNumRows(Math.max(1, numRows - 1))}
                      disabled={numRows <= 1}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 disabled:opacity-40 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="font-bold text-gray-900 text-sm font-mono w-20 text-center">{numRows} Rows</span>
                    <button
                      type="button"
                      onClick={() => setNumRows(numRows + 1)}
                      className="w-8 h-8 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 flex items-center justify-center text-gray-500 hover:text-gray-800 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>"""
content = content.replace(old_ui_header, new_ui_header)

# 10. Bay UI Render
content = content.replace(
    """            {/* Individual Bay configurator cards */}
            <div className="space-y-4">
              {bays.map((bay, idx) => (""",
    """            {/* Individual Bay configurator cards */}
            <div className="space-y-4">
              {bays.map((bay, idx) => {
                const r = Math.floor(idx / numBays);
                const c = idx % numBays;
                const labelText = numRows > 1 ? `Col ${c + 1}, Row ${r + 1}` : `Column ${idx + 1}`;
                return ("""
)

# Need to replace `<h3 className="font-bold text-gray-800 text-xs uppercase tracking-wider mb-3">Bay {idx + 1}</h3>`
content = content.replace(
    """<h3 className="font-bold text-gray-800 text-xs uppercase tracking-wider mb-3">Bay {idx + 1}</h3>""",
    """<h3 className="font-bold text-gray-800 text-xs uppercase tracking-wider mb-3">{labelText}</h3>"""
)

# And add the closing brace `})}`
content = content.replace(
    """                  </div>
                </div>
              ))}
            </div>""",
    """                  </div>
                </div>
              );
              })}
            </div>"""
)

# 11. SVG Drawing
old_svg_calc = """                      {/* Draw column/row dividers and styles */}
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

new_svg_calc = """                      {/* Grid Dividers */}
                      {Array.from({ length: numBays - 1 }).map((_, cIdx) => {
                         const bayW = (drawW - 16) / numBays;
                         const x = paddingX + 8 + (cIdx + 1) * bayW;
                         return <line key={`vdiv-${cIdx}`} x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke="#475569" strokeWidth="2.5" />;
                      })}
                      {Array.from({ length: numRows - 1 }).map((_, rIdx) => {
                         const bayH = (drawH - 16) / numRows;
                         const y = paddingY + 8 + (rIdx + 1) * bayH;
                         return <line key={`hdiv-${rIdx}`} x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke="#475569" strokeWidth="2.5" />;
                      })}

                      {/* Draw column/row dividers and styles */}
                      {bays.map((bay, idx) => {
                        const r = Math.floor(idx / numBays);
                        const c = idx % numBays;
                        const bayW = (drawW - 16) / numBays;
                        const bayH = (drawH - 16) / numRows;
                        const bayX = paddingX + 8 + c * bayW;
                        const bayY = paddingY + 8 + r * bayH;

                        return (
                          <g key={idx}>"""

content = content.replace(old_svg_calc, new_svg_calc)

# 12. DNA Summary
content = content.replace(
    '<div>• Bays Configured: {numBays} {bayDirection === "vertical" ? "vertical columns" : "horizontal rows"}</div>',
    '<div>• Bays Configured: {numBays} columns x {numRows} rows</div>'
)

# 13. Update calc dependencies for dependency arrays:
# [isCustomSize, width, depth, height, boardId, shutterBoardId, backPanelBoardId, drawerBoxBoardId, boardThickness, drawerWidth, drawerDepth, drawerHeight, quality, numBays, supportLegsCount, bays, bayDirection]
# there might be other places where it was used, so let's make sure it's fully replaced.
# We handled the main ones.

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
