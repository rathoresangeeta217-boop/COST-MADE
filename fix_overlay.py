import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_overlay = """                {/* Dragging Measurements Overlay */}
                {dragState && dragState.isDragging && (
                  (() => {
                    const bay = bays[dragState.bayIdx];
                    if (dragState.type === 'h') {
                       const offsetRel = bay.shelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.shelves || 0) + 1));
                       const yInBay = offsetRel * (dragState.bayH - 4);
                       const yAbsolute = dragState.bayY + 2 + yInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.shelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.shelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.shelves || 0) - 1 ? (bay.shelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.shelves || 0) + 1))) : 1;
                       
                       const topH = (offsetRel - prevOffset) * (dragState.bayH - 4);
                       const bottomH = (nextOffset - offsetRel) * (dragState.bayH - 4);

                       return (
                         <g pointerEvents="none">
                           <line x1={dragState.bayX} x2={dragState.bayX + dragState.bayW} y1={yAbsolute} y2={yAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Top measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>

                           {/* Bottom measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                         </g>
                       );
                    } else {
                       const offsetRel = bay.verticalShelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.verticalShelves || 0) + 1));
                       const xInBay = offsetRel * (dragState.bayW - 4);
                       const xAbsolute = dragState.bayX + 2 + xInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.verticalShelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.verticalShelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.verticalShelves || 0) - 1 ? (bay.verticalShelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.verticalShelves || 0) + 1))) : 1;

                       const leftW = (offsetRel - prevOffset) * (dragState.bayW - 4);
                       const rightW = (nextOffset - offsetRel) * (dragState.bayW - 4);

                       return (
                         <g pointerEvents="none">
                           <line y1={dragState.bayY} y2={dragState.bayY + dragState.bayH} x1={xAbsolute} x2={xAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Left measurement */}
                           <rect x={xAbsolute - leftW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute - leftW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(leftW)}mm</text>

                           {/* Right measurement */}
                           <rect x={xAbsolute + rightW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute + rightW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(rightW)}mm</text>
                         </g>
                       );
                    }
                  })()
                )}"""

new_overlay = """                {/* Dragging Measurements Overlay */}
                {dragState && dragState.isDragging && (
                  (() => {
                    const drawW = width;
                    const drawH = height;
                    const paddingX = 50;
                    const paddingY = 50;

                    if (dragState.type === 'main_v') {
                        const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                        const offsetRel = getColOffset(dragState.idx, numBays);
                        const prevOffset = dragState.idx > 0 ? getColOffset(dragState.idx - 1, numBays) : 0;
                        const nextOffset = dragState.idx < numBays - 1 ? getColOffset(dragState.idx + 1, numBays) : 1;
                        
                        const xAbsolute = paddingX + 8 + offsetRel * (drawW - 16);
                        const leftW = (offsetRel - prevOffset) * (drawW - 16);
                        const rightW = (nextOffset - offsetRel) * (drawW - 16);

                        return (
                         <g pointerEvents="none">
                           <line y1={paddingY + 8} y2={paddingY + drawH - 8} x1={xAbsolute} x2={xAbsolute} stroke="#6366f1" strokeWidth="2" />
                           <rect x={xAbsolute - leftW / 2 - 30} y={paddingY + drawH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={xAbsolute - leftW / 2} y={paddingY + drawH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(leftW)}mm</text>
                           <rect x={xAbsolute + rightW / 2 - 30} y={paddingY + drawH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={xAbsolute + rightW / 2} y={paddingY + drawH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(rightW)}mm</text>
                         </g>
                        );
                    } else if (dragState.type === 'main_h') {
                        const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                        const offsetRel = getRowOffset(dragState.idx, numRows);
                        const prevOffset = dragState.idx > 0 ? getRowOffset(dragState.idx - 1, numRows) : 0;
                        const nextOffset = dragState.idx < numRows - 1 ? getRowOffset(dragState.idx + 1, numRows) : 1;

                        const yAbsolute = paddingY + 8 + offsetRel * (drawH - 16);
                        const topH = (offsetRel - prevOffset) * (drawH - 16);
                        const bottomH = (nextOffset - offsetRel) * (drawH - 16);

                        return (
                         <g pointerEvents="none">
                           <line x1={paddingX + 8} x2={paddingX + drawW - 8} y1={yAbsolute} y2={yAbsolute} stroke="#6366f1" strokeWidth="2" />
                           <rect x={paddingX + drawW / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={paddingX + drawW / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>
                           <rect x={paddingX + drawW / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#6366f1" rx="12" />
                           <text x={paddingX + drawW / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                         </g>
                        );
                    }
                    
                    const bay = bays[dragState.bayIdx];
                    if (!bay) return null;

                    if (dragState.type === 'h') {
                       const offsetRel = bay.shelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.shelves || 0) + 1));
                       const yInBay = offsetRel * (dragState.bayH - 4);
                       const yAbsolute = dragState.bayY + 2 + yInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.shelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.shelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.shelves || 0) - 1 ? (bay.shelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.shelves || 0) + 1))) : 1;
                       
                       const topH = (offsetRel - prevOffset) * (dragState.bayH - 4);
                       const bottomH = (nextOffset - offsetRel) * (dragState.bayH - 4);

                       return (
                         <g pointerEvents="none">
                           <line x1={dragState.bayX} x2={dragState.bayX + dragState.bayW} y1={yAbsolute} y2={yAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Top measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute - topH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute - topH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(topH)}mm</text>

                           {/* Bottom measurement */}
                           <rect x={dragState.bayX + dragState.bayW / 2 - 30} y={yAbsolute + bottomH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={dragState.bayX + dragState.bayW / 2} y={yAbsolute + bottomH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(bottomH)}mm</text>
                         </g>
                       );
                    } else if (dragState.type === 'v') {
                       const offsetRel = bay.verticalShelfOffsets?.[dragState.idx] ?? ((dragState.idx + 1) / ((bay.verticalShelves || 0) + 1));
                       const xInBay = offsetRel * (dragState.bayW - 4);
                       const xAbsolute = dragState.bayX + 2 + xInBay;
                       
                       const prevOffset = dragState.idx > 0 ? (bay.verticalShelfOffsets?.[dragState.idx - 1] ?? (dragState.idx / ((bay.verticalShelves || 0) + 1))) : 0;
                       const nextOffset = dragState.idx < (bay.verticalShelves || 0) - 1 ? (bay.verticalShelfOffsets?.[dragState.idx + 1] ?? ((dragState.idx + 2) / ((bay.verticalShelves || 0) + 1))) : 1;

                       const leftW = (offsetRel - prevOffset) * (dragState.bayW - 4);
                       const rightW = (nextOffset - offsetRel) * (dragState.bayW - 4);

                       return (
                         <g pointerEvents="none">
                           <line y1={dragState.bayY} y2={dragState.bayY + dragState.bayH} x1={xAbsolute} x2={xAbsolute} stroke="#10b981" strokeWidth="2" />
                           
                           {/* Left measurement */}
                           <rect x={xAbsolute - leftW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute - leftW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(leftW)}mm</text>

                           {/* Right measurement */}
                           <rect x={xAbsolute + rightW / 2 - 30} y={dragState.bayY + dragState.bayH / 2 - 12} width="60" height="24" fill="#10b981" rx="12" />
                           <text x={xAbsolute + rightW / 2} y={dragState.bayY + dragState.bayH / 2} fill="white" fontSize="11" textAnchor="middle" dominantBaseline="middle" fontWeight="bold">{Math.round(rightW)}mm</text>
                         </g>
                       );
                    }
                    return null;
                  })()
                )}"""

content = content.replace(old_overlay, new_overlay)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
