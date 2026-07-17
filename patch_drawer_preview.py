import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """          {/* Right Side: Cost Overview */}
          <div className="xl:col-span-5 space-y-6">"""

replacement = """          {/* Right Side: Cost Overview */}
          <div className="xl:col-span-5 space-y-6">
            {/* Drawer Preview */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Drawer Blueprint
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                  <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                  <button onClick={() => setIsFullScreenDrawing(!isFullScreenDrawing)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">{isFullScreenDrawing ? "Exit Full Screen" : "Full Screen"}</button>
                </div>
              </div>
              <div className={`flex justify-center p-6 bg-slate-50 relative ${isFullScreenDrawing ? 'fixed inset-0 z-50 overflow-auto bg-slate-900/95' : 'border border-gray-200 rounded-xl overflow-hidden'}`}>
                {isFullScreenDrawing && (
                  <div className="fixed top-4 right-4 flex items-center gap-2 z-[60] bg-white p-2 rounded-xl shadow-lg border border-gray-200">
                    <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                    <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                    <button onClick={() => { setIsFullScreenDrawing(false); setZoomLevel(1); }} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Exit Full Screen</button>
                  </div>
                )}
                <svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={(drawerWidth + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  height={(drawerHeight + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  className="drop-shadow-2xl transition-all duration-200"
                  xmlns="http://www.w3.org/2000/svg"
                >
                   {/* Drawer face outer line */}
                   <rect x="0" y="0" width={drawerWidth} height={drawerHeight} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="4" rx="2" />
                   {/* Drawer face inner line */}
                   <rect x="18" y="18" width={drawerWidth-36} height={drawerHeight-36} fill="none" stroke="#64748b" strokeWidth="1" strokeDasharray="4 2"/>
                   
                   {/* Handle */}
                   {drawerHandle && (
                     <g>
                       <rect x={drawerWidth/2 - 60} y={drawerHeight/2 - 8} width="120" height="16" fill="#94a3b8" rx="8" />
                       <rect x={drawerWidth/2 - 40} y={drawerHeight/2 - 4} width="80" height="8" fill="#e2e8f0" rx="4" />
                     </g>
                   )}
                   
                   {/* Lock */}
                   {drawerLock && (
                     <g>
                       <circle cx={drawerWidth - 40} cy={40} r="12" fill="#cbd5e1" stroke="#64748b" strokeWidth="2" />
                       <rect x={drawerWidth - 42} y={38} width="4" height="6" fill="#64748b" />
                     </g>
                   )}
                   
                   {/* Dimension labels */}
                   <text x={drawerWidth / 2} y="-20" fill="#64748b" fontSize={Math.max(12, drawerWidth * 0.05)} textAnchor="middle" fontWeight="bold">{drawerWidth}mm</text>
                   <text x="-20" y={drawerHeight / 2} fill="#64748b" fontSize={Math.max(12, drawerHeight * 0.05)} textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${drawerHeight/2})`}>{drawerHeight}mm</text>
                </svg>
              </div>
            </div>"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
