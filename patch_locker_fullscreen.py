import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Locker Blueprint
                  </h2>
                </div>
              </div>
              <div className="flex justify-center p-6 bg-slate-50 relative border border-gray-200 rounded-xl overflow-hidden">
                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={(computedLockerWidth + 100) * 0.4}
                  height={(computedLockerHeight + 100) * 0.4}
                  className="drop-shadow-2xl transition-all duration-200 max-h-[600px] w-auto"
                  xmlns="http://www.w3.org/2000/svg"
                >"""

replacement = """            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 text-gray-500" />
                  <h2 className="font-semibold text-gray-900 text-sm uppercase tracking-wider">
                    Live Locker Blueprint
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
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={(computedLockerWidth + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  height={(computedLockerHeight + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  className="drop-shadow-2xl transition-all duration-200 max-h-[600px] w-auto"
                  xmlns="http://www.w3.org/2000/svg"
                >"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

