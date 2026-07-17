import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

start_str = "{/* Draw angular custom shelves */}"
end_str = "              </svg>"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

replacement = """{/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => {
                  const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
                  const cx = (s.x1 + s.x2) / 2;
                  const cy = (s.y1 + s.y2) / 2;
                  
                  const isVertical = Math.abs(s.x1 - s.x2) < 5;
                  const isHorizontal = Math.abs(s.y1 - s.y2) < 5;
                  const show4Sides = isDrawingAngular && (isVertical || isHorizontal);
                  const isAngular = !isVertical && !isHorizontal;

                  return (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="8" strokeLinecap="round" />
                     <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                     <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                     
                     {isAngular && (
                        <g>
                          <line x1={s.x1} y1={s.y2} x2={s.x2} y2={s.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" />
                          <line x1={s.x1} y1={s.y1} x2={s.x1} y2={s.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" />
                          
                          <rect x={cx - 25} y={s.y2 - 12 + (s.y1 < s.y2 ? 20 : -20)} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={cx} y={s.y2 + (s.y1 < s.y2 ? 20 : -20)} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">W: {Math.round(Math.abs(s.x2 - s.x1))}mm</text>
                          
                          <rect x={s.x1 - 25 + (s.x1 < s.x2 ? -30 : 30)} y={cy - 10} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={s.x1 + (s.x1 < s.x2 ? -30 : 30)} y={cy} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">H: {Math.round(Math.abs(s.y2 - s.y1))}mm</text>
                        </g>
                     )}

                     {show4Sides && (() => {
                        const minX = Math.min(s.x1, s.x2);
                        const maxX = Math.max(s.x1, s.x2);
                        const minY = Math.min(s.y1, s.y2);
                        const maxY = Math.max(s.y1, s.y2);

                        const leftDist = minX - 50;
                        const rightDist = (50 + width) - maxX;
                        const topDist = minY - 50;
                        const bottomDist = (50 + height) - maxY;

                        return (
                          <g>
                            {/* Left Gap */}
                            <rect x={minX - Math.max(0, leftDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={minX - Math.max(0, leftDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(Math.max(0, leftDist))}mm</text>
                            
                            {/* Right Gap */}
                            <rect x={maxX + Math.max(0, rightDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={maxX + Math.max(0, rightDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(Math.max(0, rightDist))}mm</text>

                            {/* Top Gap */}
                            <rect x={cx - 45} y={minY - Math.max(0, topDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={minY - Math.max(0, topDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(Math.max(0, topDist))}mm</text>
                            
                            {/* Bottom Gap */}
                            <rect x={cx - 45} y={maxY + Math.max(0, bottomDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={maxY + Math.max(0, bottomDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(Math.max(0, bottomDist))}mm</text>
                          </g>
                        );
                     })()}

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
                  
                  const isVertical = Math.abs(currentAngularShelf.x1 - currentAngularShelf.x2) < 5;
                  const isHorizontal = Math.abs(currentAngularShelf.y1 - currentAngularShelf.y2) < 5;
                  const show4Sides = isVertical || isHorizontal;
                  const isAngular = !isVertical && !isHorizontal;

                  return (
                    <g pointerEvents="none">
                      <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="8" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                      <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                      <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                      
                      {isAngular && (
                        <g>
                          <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y2} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" opacity="0.7" />
                          <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x1} y2={currentAngularShelf.y2} stroke="#10b981" strokeWidth="2" strokeDasharray="4,4" opacity="0.7" />
                          
                          <rect x={cx - 25} y={currentAngularShelf.y2 - 12 + (currentAngularShelf.y1 < currentAngularShelf.y2 ? 20 : -20)} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={cx} y={currentAngularShelf.y2 + (currentAngularShelf.y1 < currentAngularShelf.y2 ? 20 : -20)} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">W: {Math.round(Math.abs(currentAngularShelf.x2 - currentAngularShelf.x1))}mm</text>
                          
                          <rect x={currentAngularShelf.x1 - 25 + (currentAngularShelf.x1 < currentAngularShelf.x2 ? -30 : 30)} y={cy - 10} width="50" height="20" fill="#10b981" rx="10" />
                          <text x={currentAngularShelf.x1 + (currentAngularShelf.x1 < currentAngularShelf.x2 ? -30 : 30)} y={cy} fill="white" fontSize="10" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">H: {Math.round(Math.abs(currentAngularShelf.y2 - currentAngularShelf.y1))}mm</text>
                        </g>
                      )}

                      {show4Sides && (() => {
                        const minX = Math.min(currentAngularShelf.x1, currentAngularShelf.x2);
                        const maxX = Math.max(currentAngularShelf.x1, currentAngularShelf.x2);
                        const minY = Math.min(currentAngularShelf.y1, currentAngularShelf.y2);
                        const maxY = Math.max(currentAngularShelf.y1, currentAngularShelf.y2);

                        const leftDist = minX - 50;
                        const rightDist = (50 + width) - maxX;
                        const topDist = minY - 50;
                        const bottomDist = (50 + height) - maxY;

                        return (
                          <g>
                            <rect x={minX - Math.max(0, leftDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={minX - Math.max(0, leftDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(Math.max(0, leftDist))}mm</text>
                            
                            <rect x={maxX + Math.max(0, rightDist)/2 - 30} y={cy - 25} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={maxX + Math.max(0, rightDist)/2} y={cy - 13} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(Math.max(0, rightDist))}mm</text>

                            <rect x={cx - 45} y={minY - Math.max(0, topDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={minY - Math.max(0, topDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(Math.max(0, topDist))}mm</text>
                            
                            <rect x={cx - 45} y={maxY + Math.max(0, bottomDist)/2 - 12} width="60" height="24" fill="#3b82f6" rx="12" />
                            <text x={cx - 15} y={maxY + Math.max(0, bottomDist)/2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(Math.max(0, bottomDist))}mm</text>
                          </g>
                        );
                      })()}
                    </g>
                  );
                })()}
"""

content = content[:start_idx] + replacement + content[end_idx:]

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

