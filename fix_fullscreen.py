import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  4. Live Technical Blueprint {constructionCategory === 'metal' ? '(Metal Rack)' : ''}
                </h2>
              </div>
            </div>"""

replacement = """            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4 text-gray-500" />
                <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                  4. Live Technical Blueprint {constructionCategory === 'metal' ? '(Metal Rack)' : ''}
                </h2>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                <button onClick={() => setIsFullScreenDrawing(!isFullScreenDrawing)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">{isFullScreenDrawing ? "Exit Full Screen" : "Full Screen"}</button>
              </div>
            </div>"""

content = content.replace(target, replacement)

# Now, we need to handle isFullScreenDrawing in the JSX
# We will wrap the SVG area or use a fixed modal if isFullScreenDrawing is true
# But let's see where isFullScreenDrawing is used right now

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
