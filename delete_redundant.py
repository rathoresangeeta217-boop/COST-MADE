import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'\{/\* Component breakdown card \*/\}.*?\{/\* Hardware list breakdown card \*/\}', '{/* Hardware list breakdown card */}', content, flags=re.DOTALL)
content = re.sub(r'\{/\* Hardware list breakdown card \*/\}\s*<div className="mt-6 border-t border-slate-700 pt-4">\s*<h3 className="text-xs font-semibold uppercase text-slate-400 mb-3 tracking-wider">Hardware Breakdown</h3>\s*<div className="space-y-2">\s*\{drawerCalcData\.hardware\.map\(\(h, i\) => \(\s*<div key=\{i\} className="flex justify-between text-xs items-center">\s*<span className="text-slate-300 font-sans">\{h\.qty\}x \{h\.label\}</span>\s*<span className="font-mono text-slate-400">Rs \{h\.cost\.toFixed\(0\)\}</span>\s*</div>\s*\)\)\}\s*</div>\s*</div>', '', content, flags=re.DOTALL)

content = re.sub(r'\{/\* Hardware list breakdown card \*/\}\s*<div className="mt-6 border-t border-slate-700 pt-4">\s*<h3 className="text-xs font-semibold uppercase text-slate-400 mb-3 tracking-wider">Hardware Breakdown</h3>\s*<div className="space-y-2">\s*\{lockerCalcData\.hardware\.map\(\(h, i\) => \(\s*<div key=\{i\} className="flex justify-between text-xs items-center">\s*<span className="text-slate-300 font-sans">\{h\.qty\}x \{h\.label\}</span>\s*<span className="font-mono text-slate-400">Rs \{h\.cost\.toFixed\(0\)\}</span>\s*</div>\s*\)\)\}\s*</div>\s*</div>', '', content, flags=re.DOTALL)


with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
