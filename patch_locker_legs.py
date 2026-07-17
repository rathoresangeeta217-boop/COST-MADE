import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# State
state_target = """  const [lockerCncDesign, setLockerCncDesign] = useState<boolean>(false);"""
state_replace = """  const [lockerCncDesign, setLockerCncDesign] = useState<boolean>(false);
  const [lockerAddBottomLegs, setLockerAddBottomLegs] = useState<boolean>(false);"""
content = content.replace(state_target, state_replace)

# UI
ui_target = """                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerCncDesign} onChange={(e) => setLockerCncDesign(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add CNC Cutout</span>
                  </label>
                </div>"""
ui_replace = """                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerCncDesign} onChange={(e) => setLockerCncDesign(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add CNC Cutout</span>
                  </label>
                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerAddBottomLegs} onChange={(e) => setLockerAddBottomLegs(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add Bottom Legs (150mm)</span>
                  </label>
                </div>"""
content = content.replace(ui_target, ui_replace)

# SVG ViewBox
svg_target = """                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerHeight + 100) * 0.4}"""
svg_replace = """                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100 + (lockerAddBottomLegs ? 150 : 0)}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerHeight + 100 + (lockerAddBottomLegs ? 150 : 0)) * 0.4}"""
content = content.replace(svg_target, svg_replace)

# SVG Frame
svg_frame_target = """                   {/* Main Frame */}
                   <rect x="0" y="0" width={computedLockerWidth} height={computedLockerHeight} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" rx="4" />
                   
                   {/* Columns */}
                   {Array.from({ length: lockerColumns }).map((_, cIdx) => {"""
svg_frame_replace = """                   {/* Main Frame */}
                   <rect x="0" y="0" width={computedLockerWidth} height={computedLockerHeight + (lockerAddBottomLegs ? 150 : 0)} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" rx="4" />
                   
                   {/* Columns */}
                   {Array.from({ length: lockerColumns }).map((_, cIdx) => {"""
content = content.replace(svg_frame_target, svg_frame_replace)

# SVG Column Dividers
svg_col_target = """                         {/* Vertical Divider */}
                         {cIdx > 0 && <line x1={colX} y1="0" x2={colX} y2={computedLockerHeight} stroke="#94a3b8" strokeWidth="4" />}"""
svg_col_replace = """                         {/* Vertical Divider */}
                         {cIdx > 0 && <line x1={colX} y1="0" x2={colX} y2={computedLockerHeight + (lockerAddBottomLegs ? 150 : 0)} stroke="#94a3b8" strokeWidth="4" />}"""
content = content.replace(svg_col_target, svg_col_replace)

# SVG Legs
svg_legs_target = """                   {/* Dimension labels */}
                   <text x={computedLockerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(16, computedLockerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{computedLockerWidth}mm</text>
                   <text x="-20" y={computedLockerHeight / 2} fill="#64748b" fontSize={Math.max(16, computedLockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${computedLockerHeight/2})`}>{computedLockerHeight}mm</text>
                </svg>"""
svg_legs_replace = """                   {lockerAddBottomLegs && (
                     <g>
                       {/* Left Leg */}
                       <rect x={0} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                       <rect x="-5" y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       
                       {/* Right Leg */}
                       <rect x={computedLockerWidth - 40} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                       <rect x={computedLockerWidth - 45} y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                       
                       {/* Additional middle legs for larger width */}
                       {computedLockerWidth >= 1800 && (
                         <>
                           <rect x={computedLockerWidth / 2 - 20} y={computedLockerHeight} width={40} height={150} fill="#f1f5f9" stroke="#64748b" strokeWidth="6" />
                           <rect x={computedLockerWidth / 2 - 25} y={computedLockerHeight + 150 - 20} width={50} height={20} fill="#334155" rx="4" />
                         </>
                       )}

                       {/* Dimension labels for legs */}
                       <line x1="-30" y1={computedLockerHeight} x2="-20" y2={computedLockerHeight} stroke="#64748b" strokeWidth="2" />
                       <line x1="-30" y1={computedLockerHeight + 150} x2="-20" y2={computedLockerHeight + 150} stroke="#64748b" strokeWidth="2" />
                       <line x1="-25" y1={computedLockerHeight} x2="-25" y2={computedLockerHeight + 150} stroke="#64748b" strokeWidth="2" strokeDasharray="4" />
                       <text x="-35" y={computedLockerHeight + 75} fill="#64748b" fontSize={Math.max(16, computedLockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -35 ${computedLockerHeight + 75})`}>150mm</text>
                     </g>
                   )}
                   {/* Dimension labels */}
                   <text x={computedLockerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(16, computedLockerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{computedLockerWidth}mm</text>
                   <text x="-20" y={computedLockerHeight / 2} fill="#64748b" fontSize={Math.max(16, computedLockerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${computedLockerHeight/2})`}>{computedLockerHeight}mm</text>
                </svg>"""
content = content.replace(svg_legs_target, svg_legs_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
