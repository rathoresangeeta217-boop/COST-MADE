import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                {/* Draw angular custom shelves */}
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
                })}"""

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
                     
                     <circle cx={s.x1} cy={s.y1} r="8" fill="#f59e0b" stroke="white" strokeWidth="2" cursor="pointer"
                        onPointerDown={(e) => {
                           e.stopPropagation();
                           if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                           setDragState({
                               bayIdx: -1, type: 'angular_endpoint', idx: 1, startX: e.clientX, startY: e.clientY,
                               bayX: 0, bayY: 0, bayW: 0, bayH: 0, isDragging: false, partitionId: '', shelfId: s.id
                           });
                        }}
                     />
                     <circle cx={s.x2} cy={s.y2} r="8" fill="#f59e0b" stroke="white" strokeWidth="2" cursor="pointer"
                        onPointerDown={(e) => {
                           e.stopPropagation();
                           if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                           setDragState({
                               bayIdx: -1, type: 'angular_endpoint', idx: 2, startX: e.clientX, startY: e.clientY,
                               bayX: 0, bayY: 0, bayW: 0, bayH: 0, isDragging: false, partitionId: '', shelfId: s.id
                           });
                        }}
                     />
                     
                     {isDrawingAngular && (
                       <circle cx={cx} cy={cy - 20} r="10" fill="#ef4444" cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }} />
                     )}
                  </g>
                  );
                })}"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
