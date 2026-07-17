import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace container
content = content.replace("className={`flex justify-center p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 items-center' : 'relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}",
                          "className={`p-6 ${isFullScreenDrawing ? 'fixed inset-0 z-[100] overflow-auto bg-slate-900/95 flex' : 'flex justify-center relative bg-slate-50 border border-gray-200 rounded-xl overflow-hidden'}`}")

# Add m-auto to SVGs
metal_svg = r'className={`drop-shadow-md transition-all duration-200 \$\{isFullScreenDrawing \? "" : "max-h-\[600px\] w-auto"\}`}'
metal_replace = r'className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}'
content = re.sub(metal_svg, metal_replace, content)

wood_svg = r'className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "" : "max-h-\[600px\] w-auto"\}`}'
wood_replace = r'className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}'
content = re.sub(wood_svg, wood_replace, content)


with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

