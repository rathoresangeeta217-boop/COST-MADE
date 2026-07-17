import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                  })()
                )}
              </svg>"""

replacement = """                  })()
                )}

                {/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="18" strokeLinecap="round" />
                     {isDrawingAngular && (
                       <circle cx={s.x2} cy={s.y2} r="12" fill="#ef4444" cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }} />
                     )}
                  </g>
                ))}
                {currentAngularShelf && (
                  <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="18" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                )}
              </svg>"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
