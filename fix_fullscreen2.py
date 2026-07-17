import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """            <div className="flex justify-center p-6 bg-slate-50 border border-gray-200 rounded-xl overflow-hidden relative">"""

replacement = """            <div className={`flex justify-center p-6 bg-slate-50 relative ${isFullScreenDrawing ? 'fixed inset-0 z-50 overflow-auto bg-slate-900/95' : 'border border-gray-200 rounded-xl overflow-hidden'}`}>
              {isFullScreenDrawing && (
                <div className="fixed top-4 right-4 flex items-center gap-2 z-[60] bg-white p-2 rounded-xl shadow-lg border border-gray-200">
                  <button onClick={() => setZoomLevel(prev => prev + 0.2)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom In</button>
                  <button onClick={() => setZoomLevel(prev => Math.max(0.4, prev - 0.2))} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Zoom Out</button>
                  <button onClick={() => { setIsFullScreenDrawing(false); setZoomLevel(1); }} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 text-xs font-semibold uppercase tracking-wider border border-gray-200">Exit Full Screen</button>
                </div>
              )}"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
