import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# find the block starting with {/* Draw angular custom shelves */}
# and ending at the end of the currentAngularShelf block
start_str = "{/* Draw angular custom shelves */}"
end_str = "})()}"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

original_block = content[start_idx:end_idx]

replacement = """{/* Draw angular custom shelves */}
                {angularShelves.map((s, i) => {
                  const length = Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
                  const cx = (s.x1 + s.x2) / 2;
                  const cy = (s.y1 + s.y2) / 2;
                  
                  const isVertical = Math.abs(s.x1 - s.x2) < 5;
                  const isHorizontal = Math.abs(s.y1 - s.y2) < 5;

                  return (
                  <g key={s.id}>
                     <line x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} stroke="#f59e0b" strokeWidth="8" strokeLinecap="round" />
                     <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                     <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>
                     
                     {isDrawingAngular && isVertical && (() => {
                        const leftW = cx - 50;
                        const rightW = (50 + width) - cx;
                        return (
                          <g>
                            <rect x={cx - leftW / 2 - 30} y={cy - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx - leftW / 2} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(leftW)}mm</text>
                            
                            <rect x={cx + rightW / 2 - 30} y={cy - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx + rightW / 2} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(rightW)}mm</text>
                          </g>
                        );
                     })()}

                     {isDrawingAngular && isHorizontal && (() => {
                        const topH = cy - 50;
                        const bottomH = (50 + height) - cy;
                        return (
                          <g>
                            <rect x={cx - 30} y={cy - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx} y={cy - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(topH)}mm</text>
                            
                            <rect x={cx - 30} y={cy + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx} y={cy + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(bottomH)}mm</text>
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

                  return (
                    <g pointerEvents="none">
                      <line x1={currentAngularShelf.x1} y1={currentAngularShelf.y1} x2={currentAngularShelf.x2} y2={currentAngularShelf.y2} stroke="#f59e0b" strokeWidth="8" strokeDasharray="5,5" opacity="0.7" strokeLinecap="round" />
                      <rect x={cx - 30} y={cy - 12} width="60" height="24" fill="#f59e0b" rx="12" />
                      <text x={cx} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(length)}mm</text>

                      {isVertical && (() => {
                        const leftW = cx - 50;
                        const rightW = (50 + width) - cx;
                        return (
                          <g>
                            <rect x={cx - leftW / 2 - 30} y={cy - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx - leftW / 2} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">L: {Math.round(leftW)}mm</text>
                            
                            <rect x={cx + rightW / 2 - 30} y={cy - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx + rightW / 2} y={cy} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">R: {Math.round(rightW)}mm</text>
                          </g>
                        );
                      })()}

                      {isHorizontal && (() => {
                        const topH = cy - 50;
                        const bottomH = (50 + height) - cy;
                        return (
                          <g>
                            <rect x={cx - 30} y={cy - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx} y={cy - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">T: {Math.round(topH)}mm</text>
                            
                            <rect x={cx - 30} y={cy + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                            <text x={cx} y={cy + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">B: {Math.round(bottomH)}mm</text>
                          </g>
                        );
                      })()}
                    </g>
                  );
                })()}"""

content = content[:start_idx] + replacement + content[end_idx:]

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
