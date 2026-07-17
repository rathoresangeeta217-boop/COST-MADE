import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                {/* Draw angular custom shelves */}
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

replacement = """                {/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => {
                  const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
                  const cx = (s.x1 + s.x2) / 2;
                  const cy = (s.y1 + s.y2) / 2;
                  return (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="18" strokeLinecap="round" />
                     <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                     <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                     {isDrawingAngular && (
                       <circle cx={s.x2} cy={s.y2} r="12" fill="#ef4444" cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }} />
                     )}
                  </g>
                  );
                })}
                {currentAngularShelf && (() => {
                  const length = Math.hypot(currentAngularShelf.x2 - currentAngularShelf.x1, currentAngularShelf.y2 - currentAngularShelf.y1);
                  const cx = (currentAngularShelf.x1 + currentAngularShelf.x2) / 2;
                  const cy = (currentAngularShelf.y1 + currentAngularShelf.y2) / 2;
                  return (
                    <g pointerEvents="none">
                      <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="18" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                      <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                      <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                    </g>
                  );
                })()}
              </svg>"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
