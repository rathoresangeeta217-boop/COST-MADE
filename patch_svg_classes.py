import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Replace the wrapper div class to ensure it centers and fills properly
content = content.replace("isFullScreenDrawing ? 'fixed inset-0 z-50 overflow-auto bg-slate-900/95' : 'border border-gray-200 rounded-xl overflow-hidden'",
                          "isFullScreenDrawing ? 'fixed inset-0 z-50 overflow-auto bg-slate-900/95 items-center' : 'border border-gray-200 rounded-xl overflow-hidden'")

# 2. Replace SVG classes
content = content.replace('className="max-h-[600px] w-auto drop-shadow-md"',
                          'className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "w-full max-h-[90vh]" : "max-h-[600px] w-auto"}`}')
content = content.replace('className="drop-shadow-2xl transition-all duration-200 max-h-[600px] w-auto"',
                          'className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "w-full max-h-[90vh]" : "max-h-[600px] w-auto"}`}')

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

