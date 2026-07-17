import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """          {/* Section 4: Live 2D Front View Vector Preview */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  4. Live Technical Blueprint {constructionCategory === 'metal' ? '(Metal Rack)' : ''}
                </h2>
              </div>
            </div>
            
            <div className="flex justify-center p-6 bg-slate-50 border border-gray-200 rounded-xl overflow-hidden relative">
              {constructionCategory === "metal" ? (
                 <svg width="100%" height="auto" viewBox={`-50 -50 ${width + 100} ${height + 100}`} className="max-h-[600px] w-auto drop-shadow-md">
                   <rect x="0" y="0" width={width} height={height} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="2" />
                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height} fill="#94a3b8" />
                   )}
                   {/* Horizontal Shelves */}
                   {Array.from({ length: numRows + 1 }).map((_, i) => (
                     <rect key={`shelf-${i}`} x="0" y={i * (height / numRows) - (i === numRows ? 20 : 0)} width={width} height={20} fill={shelfMaterialType === 'metal' ? '#64748b' : '#d97706'} />
                   ))}
                   {/* Dimension labels */}
                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>
              ) : (
                <svg"""

# We search for the start of the SVG block
content = re.sub(
    r'          \{\/\* Section 4: Live 2D Front View Vector Preview \*\/.*?<svg',
    replacement,
    content,
    flags=re.DOTALL
)

# Find the closing </svg> and add )}
content = re.sub(
    r'              <\/svg>',
    r'              </svg>\n              )}',
    content
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
