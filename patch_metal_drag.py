import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """              {constructionCategory === "metal" ? (
                 <svg width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4} height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4} viewBox={`-50 -50 ${width + 100} ${height + 100}`} className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}>
                   <rect x="0" y="0" width={width} height={height} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="2" />
                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height} fill="#94a3b8" />
                   )}
                   {/* Horizontal Shelves */}
                   {Array.from({ length: numRows + 1 }).map((_, i) => (
                     <rect key={`shelf-${i}`} x="0" y={i * (height / numRows) - (i === numRows ? 20 : 0)} width={width} height={20} fill={shelfMaterialType === 'metal' ? '#64748b' : '#d97706'} />
                   ))}
                   {/* Dimension labels */}
                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>"""

replace = """              {constructionCategory === "metal" ? (
                 <svg 
                   width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4} 
                   height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4} 
                   viewBox={`-50 -50 ${width + 100} ${height + 100}`} 
                   className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                   onPointerMove={(e) => {
                     if (!dragState) return;
                     e.preventDefault();
                     const { type, idx, startY } = dragState;
                     const dy = e.clientY - startY;
                     if (Math.abs(dy) > 3 && !dragState.isDragging) {
                       setDragState({...dragState, isDragging: true});
                       isDraggingRef.current = true;
                     }
                     if (!dragState.isDragging) return;
                     
                     const scale = 1 / (0.4 * (isFullScreenDrawing ? zoomLevel : 1));
                     if (type === 'main_h') {
                       let currentRel = rowOffsets[idx];
                       if (currentRel === undefined) {
                          currentRel = (idx + 1) / numRows;
                       }
                       let deltaRel = (dy * scale) / height;
                       let newRel = currentRel + deltaRel;
                       let prevRel = idx > 0 ? (rowOffsets[idx - 1] ?? (idx / numRows)) : 0;
                       let nextRel = idx < numRows - 1 ? (rowOffsets[idx + 1] ?? ((idx + 2) / numRows)) : 1;
                       newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));
                       setRowOffsets(prev => ({ ...prev, [idx]: newRel }));
                       setDragState({...dragState, startY: e.clientY});
                     }
                   }}
                   onPointerUp={(e) => {
                     if (dragState) {
                       if (isDraggingRef.current) e.preventDefault();
                       setDragState(null);
                       isDraggingRef.current = false;
                     }
                   }}
                   onPointerLeave={(e) => {
                     if (dragState) {
                       setDragState(null);
                       isDraggingRef.current = false;
                     }
                   }}
                 >
                   <rect x="0" y="0" width={width} height={height} fill="#f1f5f9" stroke="#94a3b8" strokeWidth="2" />
                   {/* Vertical angles */}
                   <rect x="0" y="0" width={40} height={height} fill="#64748b" />
                   <rect x={width - 40} y="0" width={40} height={height} fill="#64748b" />
                   {addVerticalPartitionMiddle && (
                     <rect x={(width / 2) - 20} y="0" width={40} height={height} fill="#94a3b8" />
                   )}
                   {/* Horizontal Shelves */}
                   {Array.from({ length: numRows + 1 }).map((_, i) => {
                     const isFirst = i === 0;
                     const isLast = i === numRows;
                     let y = 0;
                     if (isFirst) y = 0;
                     else if (isLast) y = height - 20;
                     else {
                       const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                       y = getRowOffset(i - 1, numRows) * height - 10;
                     }
                     return (
                       <g key={`shelf-${i}`}>
                         <rect x="0" y={y} width={width} height={20} fill={shelfMaterialType === 'metal' ? '#64748b' : '#d97706'} />
                         {!isFirst && !isLast && (
                           <rect 
                             x="0" y={y - 10} width={width} height={40} 
                             fill="transparent" 
                             className={dragState?.type === 'main_h' && dragState?.idx === i - 1 ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"}
                             onPointerDown={(e) => {
                               setDragState({ bayIdx: -1, type: 'main_h', idx: i - 1, startX: e.clientX, startY: e.clientY, bayW: 0, bayH: 0, bayX: 0, bayY: 0, isDragging: false });
                               if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                               e.stopPropagation();
                             }}
                           />
                         )}
                       </g>
                     )
                   })}
                   
                   {/* Measurement overlay when dragging */}
                   {(() => {
                      if (dragState?.isDragging && dragState.type === 'main_h') {
                          const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                          const offsetRel = getRowOffset(dragState.idx, numRows);
                          const prevOffset = dragState.idx > 0 ? getRowOffset(dragState.idx - 1, numRows) : 0;
                          const nextOffset = dragState.idx < numRows - 1 ? getRowOffset(dragState.idx + 1, numRows) : 1;
                          
                          const yAbsolute = offsetRel * height;
                          const topH = (offsetRel - prevOffset) * height;
                          const bottomH = (nextOffset - offsetRel) * height;
                          
                          return (
                            <g pointerEvents="none">
                               <line x1="0" x2={width} y1={yAbsolute} y2={yAbsolute} stroke="#10b981" strokeWidth="2" />
                               <rect x={width / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                               <text x={width / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>
                               <rect x={width / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                               <text x={width / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                            </g>
                          )
                      }
                      return null;
                   })()}

                   {/* Dimension labels */}
                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>"""

content = content.replace(target, replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

