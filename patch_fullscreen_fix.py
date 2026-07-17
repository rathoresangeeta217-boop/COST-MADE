import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = r"className=\{`flex justify-center p-6 bg-slate-50 relative \$\{isFullScreenDrawing \? 'fixed inset-0 z-50 overflow-auto bg-slate-900/95 items-center' : 'border border-gray-200 rounded-xl overflow-hidden'\}`\}"
replacement = r"className={`flex justify-center p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 items-center' : 'relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}"

content = re.sub(target, replacement, content)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

