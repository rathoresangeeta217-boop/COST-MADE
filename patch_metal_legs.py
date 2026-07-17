import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Add state
state_target = """  const [addVerticalPartitionMiddle, setAddVerticalPartitionMiddle] = useState<boolean>(false);"""
state_replace = """  const [addVerticalPartitionMiddle, setAddVerticalPartitionMiddle] = useState<boolean>(false);
  const [addMetalBottomLegs, setAddMetalBottomLegs] = useState<boolean>(false);"""
content = content.replace(state_target, state_replace)

# Add to config saving
config_target = """                    boardThickness, innerMica, outerMica, numBays, supportLegsCount,
                    bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId, pieceOverrides, thicknessOverrides"""
config_replace = """                    boardThickness, innerMica, outerMica, numBays, supportLegsCount,
                    bays, shutterBoardId, backPanelBoardId, drawerBoxBoardId, pieceOverrides, thicknessOverrides,
                    constructionCategory, angleThickness, shelfMaterialType, woodenShelfId, woodenShelfThickness, addVerticalPartitionMiddle, addMetalBottomLegs"""
content = content.replace(config_target, config_replace)

# Also load from config
load_config_target = """        if (c.bays !== undefined) setBays(c.bays);
      }
    }
  }, [editItemId, projectId, projects]);"""
load_config_replace = """        if (c.bays !== undefined) setBays(c.bays);
        
        if (c.constructionCategory !== undefined) setConstructionCategory(c.constructionCategory);
        if (c.angleThickness !== undefined) setAngleThickness(c.angleThickness);
        if (c.shelfMaterialType !== undefined) setShelfMaterialType(c.shelfMaterialType);
        if (c.woodenShelfId !== undefined) setWoodenShelfId(c.woodenShelfId);
        if (c.woodenShelfThickness !== undefined) setWoodenShelfThickness(c.woodenShelfThickness);
        if (c.addVerticalPartitionMiddle !== undefined) setAddVerticalPartitionMiddle(c.addVerticalPartitionMiddle);
        if (c.addMetalBottomLegs !== undefined) setAddMetalBottomLegs(c.addMetalBottomLegs);
      }
    }
  }, [editItemId, projectId, projects]);"""
content = content.replace(load_config_target, load_config_replace)

# UI modification
ui_target = """                  <div className="flex items-center pt-5">
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addVerticalPartitionMiddle}
                        onChange={(e) => setAddVerticalPartitionMiddle(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Vertical Partition at Middle
                    </label>
                  </div>"""
ui_replace = """                  <div className="flex flex-col gap-3 pt-5">
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addVerticalPartitionMiddle}
                        onChange={(e) => setAddVerticalPartitionMiddle(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Vertical Partition at Middle
                    </label>
                    <label className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer">
                      <input
                        type="checkbox"
                        checked={addMetalBottomLegs}
                        onChange={(e) => setAddMetalBottomLegs(e.target.checked)}
                        className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                      />
                      Add Bottom Legs (150mm)
                    </label>
                  </div>"""
content = content.replace(ui_target, ui_replace)

# SVG modification
svg_target = """              {constructionCategory === "metal" ? (
                 <svg 
                   width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4} 
                   height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4} 
                   viewBox={`-50 -50 ${width + 100} ${height + 100}`} 
                   className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}"""

svg_replace = """              {constructionCategory === "metal" ? (
                 <svg 
                   width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4} 
                   height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100 + (addMetalBottomLegs ? 150 : 0)) * 0.4} 
                   viewBox={`-50 -50 ${width + 100} ${height + 100 + (addMetalBottomLegs ? 150 : 0)}`} 
                   className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}"""
content = content.replace(svg_target, svg_replace)

svg_target2 = """                   const viewBoxHeight = height + 100;
                     const scale = viewBoxHeight / rect.height;"""
svg_replace2 = """                   const viewBoxHeight = height + 100 + (addMetalBottomLegs ? 150 : 0);
                     const scale = viewBoxHeight / rect.height;"""
content = content.replace(svg_target2, svg_replace2)

svg_target3 = """                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height} fill="#94a3b8" />
                   )}"""

svg_replace3 = """                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height + (addMetalBottomLegs ? 150 : 0)} fill="#94a3b8" />
                   )}
                   {addMetalBottomLegs && (
                     <g>
                       {/* Rubber shoes at the bottom */}
                       <rect x="-5" y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       <rect x={width - 45} y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       {addVerticalPartitionMiddle && (
                         <rect x={(width / 2) - 25} y={height + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       )}
                       {/* Dimension labels for legs */}
                       <line x1="-30" y1={height} x2="-20" y2={height} stroke="#64748b" strokeWidth="2" />
                       <line x1="-30" y1={height + 150} x2="-20" y2={height + 150} stroke="#64748b" strokeWidth="2" />
                       <line x1="-25" y1={height} x2="-25" y2={height + 150} stroke="#64748b" strokeWidth="2" strokeDasharray="4" />
                       <text x="-35" y={height + 75} fill="#64748b" fontSize="16" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -35 ${height + 75})`}>150mm</text>
                     </g>
                   )}"""
content = content.replace(svg_target3, svg_replace3)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

