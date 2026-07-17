import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                     {isDrawingAngular && (
                       <circle cx={cx} cy={cy - 20} r="10" fill="#ef4444" cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }} />
                     )}"""

replacement = """                     {isDrawingAngular && (
                       <g cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }}>
                         <circle cx={cx} cy={cy - 20} r="10" fill="#ef4444" />
                         <text x={cx} y={cy - 19} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">X</text>
                       </g>
                     )}"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
