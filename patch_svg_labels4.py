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
                       <g cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }}>
                         <circle cx={cx} cy={cy - 20} r="10" fill="#ef4444" />
                         <text x={cx} y={cy - 19} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">X</text>
                       </g>
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
                })()}"""

replacement = """                {/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => {
                  const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
                  const cx = (s.x1 + s.x2) / 2;
                  const cy = (s.y1 + s.y2) / 2;
                  
                  const isLeft1 = s.x1 <= s.x2;
                  const align1 = isLeft1 ? "end" : "start";
                  const offX1 = isLeft1 ? -15 : 15;
                  const align2 = !isLeft1 ? "end" : "start";
                  const offX2 = !isLeft1 ? -15 : 15;

                  return (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="8" strokeLinecap="round" />
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
                       <g pointerEvents="none">
                          <rect x={s.x1 + offX1 + (isLeft1 ? -65 : 5)} y={s.y1 - 42} width="60" height="56" fill="rgba(255,255,255,0.85)" rx="4" />
                          <text x={s.x1 + offX1} y={s.y1 - 30} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">T: {Math.round(Math.max(0, s.y1 - 50))}mm</text>
                          <text x={s.x1 + offX1} y={s.y1 - 18} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">B: {Math.round(Math.max(0, 50 + height - s.y1))}mm</text>
                          <text x={s.x1 + offX1} y={s.y1 - 6} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">L: {Math.round(Math.max(0, s.x1 - 50))}mm</text>
                          <text x={s.x1 + offX1} y={s.y1 + 6} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">R: {Math.round(Math.max(0, 50 + width - s.x1))}mm</text>
                          
                          <rect x={s.x2 + offX2 + (!isLeft1 ? -65 : 5)} y={s.y2 - 42} width="60" height="56" fill="rgba(255,255,255,0.85)" rx="4" />
                          <text x={s.x2 + offX2} y={s.y2 - 30} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">T: {Math.round(Math.max(0, s.y2 - 50))}mm</text>
                          <text x={s.x2 + offX2} y={s.y2 - 18} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">B: {Math.round(Math.max(0, 50 + height - s.y2))}mm</text>
                          <text x={s.x2 + offX2} y={s.y2 - 6} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">L: {Math.round(Math.max(0, s.x2 - 50))}mm</text>
                          <text x={s.x2 + offX2} y={s.y2 + 6} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">R: {Math.round(Math.max(0, 50 + width - s.x2))}mm</text>
                       </g>
                     )}

                     {isDrawingAngular && (
                       <g cursor="pointer" onClick={(e) => {
                          e.stopPropagation();
                          setAngularShelves(prev => prev.filter(x => x.id !== s.id));
                       }}>
                         <circle cx={cx} cy={cy - 25} r="12" fill="#ef4444" />
                         <text x={cx} y={cy - 24} fill="white" fontSize="12" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">X</text>
                       </g>
                     )}
                  </g>
                  );
                })}
                {currentAngularShelf && (() => {
                  const length = Math.hypot(currentAngularShelf.x2 - currentAngularShelf.x1, currentAngularShelf.y2 - currentAngularShelf.y1);
                  const cx = (currentAngularShelf.x1 + currentAngularShelf.x2) / 2;
                  const cy = (currentAngularShelf.y1 + currentAngularShelf.y2) / 2;
                  
                  const isLeft1 = currentAngularShelf.x1 <= currentAngularShelf.x2;
                  const align1 = isLeft1 ? "end" : "start";
                  const offX1 = isLeft1 ? -15 : 15;
                  const align2 = !isLeft1 ? "end" : "start";
                  const offX2 = !isLeft1 ? -15 : 15;

                  return (
                    <g pointerEvents="none">
                      <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="8" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                      <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                      <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>

                      <rect x={currentAngularShelf.x1 + offX1 + (isLeft1 ? -65 : 5)} y={currentAngularShelf.y1 - 42} width="60" height="56" fill="rgba(255,255,255,0.85)" rx="4" />
                      <text x={currentAngularShelf.x1 + offX1} y={currentAngularShelf.y1 - 30} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">T: {Math.round(Math.max(0, currentAngularShelf.y1 - 50))}mm</text>
                      <text x={currentAngularShelf.x1 + offX1} y={currentAngularShelf.y1 - 18} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">B: {Math.round(Math.max(0, 50 + height - currentAngularShelf.y1))}mm</text>
                      <text x={currentAngularShelf.x1 + offX1} y={currentAngularShelf.y1 - 6} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">L: {Math.round(Math.max(0, currentAngularShelf.x1 - 50))}mm</text>
                      <text x={currentAngularShelf.x1 + offX1} y={currentAngularShelf.y1 + 6} fill="#64748b" fontSize="10" textAnchor={align1} fontWeight="bold">R: {Math.round(Math.max(0, 50 + width - currentAngularShelf.x1))}mm</text>
                      
                      <rect x={currentAngularShelf.x2 + offX2 + (!isLeft1 ? -65 : 5)} y={currentAngularShelf.y2 - 42} width="60" height="56" fill="rgba(255,255,255,0.85)" rx="4" />
                      <text x={currentAngularShelf.x2 + offX2} y={currentAngularShelf.y2 - 30} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">T: {Math.round(Math.max(0, currentAngularShelf.y2 - 50))}mm</text>
                      <text x={currentAngularShelf.x2 + offX2} y={currentAngularShelf.y2 - 18} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">B: {Math.round(Math.max(0, 50 + height - currentAngularShelf.y2))}mm</text>
                      <text x={currentAngularShelf.x2 + offX2} y={currentAngularShelf.y2 - 6} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">L: {Math.round(Math.max(0, currentAngularShelf.x2 - 50))}mm</text>
                      <text x={currentAngularShelf.x2 + offX2} y={currentAngularShelf.y2 + 6} fill="#64748b" fontSize="10" textAnchor={align2} fontWeight="bold">R: {Math.round(Math.max(0, 50 + width - currentAngularShelf.x2))}mm</text>
                    </g>
                  );
                })()}"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
