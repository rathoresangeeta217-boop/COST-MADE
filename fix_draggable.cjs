const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// 1. Add to ColumnConfig
content = content.replace(
  /removedPartitions\?: string\[\];/,
  `removedPartitions?: string[];\n  shelfOffsets?: Record<number, number>;\n  verticalShelfOffsets?: Record<number, number>;`
);

// 2. Add dragState and getShelf utils
content = content.replace(
  /const togglePartition = /,
  `const [dragState, setDragState] = useState<{
    bayIdx: number;
    type: 'h' | 'v';
    idx: number;
    startX: number;
    startY: number;
    bayX: number;
    bayY: number;
    bayW: number;
    bayH: number;
    isDragging: boolean;
    partitionId: string;
  } | null>(null);

  const getShelfY = (bay: ColumnConfig, sIdx: number, baseH: number, baseY: number) => {
    if (bay.shelfOffsets?.[sIdx] !== undefined) {
      return baseY + 2 + bay.shelfOffsets[sIdx] * baseH;
    }
    return baseY + 2 + ((sIdx + 1) * baseH) / ((bay.shelves || 0) + 1);
  };

  const getVerticalShelfX = (bay: ColumnConfig, vIdx: number, baseW: number, baseX: number) => {
    if (bay.verticalShelfOffsets?.[vIdx] !== undefined) {
      return baseX + 2 + bay.verticalShelfOffsets[vIdx] * baseW;
    }
    return baseX + 2 + ((vIdx + 1) * baseW) / ((bay.verticalShelves || 0) + 1);
  };

  const togglePartition = `
);

// 3. Add pointer events to SVG
content = content.replace(
  /<svg\n\s+width="100%"\n\s+height="100%"\n\s+viewBox=\{`-20 -20 \$\{overallWidth \+ 40\} \$\{height \+ 150\}`\}\n\s+className="bg-slate-900 rounded-lg shadow-inner"/,
  `<svg
                width="100%"
                height="100%"
                viewBox={\`-20 -20 \${overallWidth + 40} \${height + 150}\`}
                className="bg-slate-900 rounded-lg shadow-inner touch-none"
                onPointerMove={(e) => {
                  if (!dragState) return;
                  const dx = e.clientX - dragState.startX;
                  const dy = e.clientY - dragState.startY;
                  if (!dragState.isDragging && (Math.abs(dx) > 3 || Math.abs(dy) > 3)) {
                      setDragState(prev => prev ? { ...prev, isDragging: true } : null);
                  }
                  if (dragState.isDragging) {
                      const svgRect = e.currentTarget.getBoundingClientRect();
                      const scaleX = (overallWidth + 40) / svgRect.width;
                      const scaleY = (height + 150) / svgRect.height;
                      
                      const xInSvg = (e.clientX - svgRect.left) * scaleX - 20; 
                      const yInSvg = (e.clientY - svgRect.top) * scaleY - 20;
                      
                      setBays(prev => {
                          const newBays = [...prev];
                          const bay = { ...newBays[dragState.bayIdx] };
                          
                          if (dragState.type === 'h') {
                              const offsets = { ...(bay.shelfOffsets || {}) };
                              let pct = (yInSvg - dragState.bayY) / (dragState.bayH - 4);
                              pct = Math.max(0.02, Math.min(0.98, pct));
                              offsets[dragState.idx] = pct;
                              bay.shelfOffsets = offsets;
                          } else {
                              const offsets = { ...(bay.verticalShelfOffsets || {}) };
                              let pct = (xInSvg - dragState.bayX) / (dragState.bayW - 4);
                              pct = Math.max(0.02, Math.min(0.98, pct));
                              offsets[dragState.idx] = pct;
                              bay.verticalShelfOffsets = offsets;
                          }
                          newBays[dragState.bayIdx] = bay;
                          return newBays;
                      });
                  }
                }}
                onPointerUp={() => {
                  if (dragState) {
                      if (!dragState.isDragging) {
                          togglePartition(dragState.partitionId, dragState.bayIdx);
                      }
                      setDragState(null);
                  }
                }}
                onPointerLeave={() => {
                  if (dragState) setDragState(null);
                }}`
);

// 4. Update the "open" bay drawing
const oldOpenSvgRegex = /\{\/\* Draw horizontal open shelves \(segmented\) \*\/\}.*?return elements;\s*\}\)\(\)\}/s;
const newOpenSvg = `{/* Draw horizontal and vertical open shelves (segmented & draggable) */}
                                {(() => {
                                  const cols = (bay.verticalShelves || 0) + 1;
                                  const rows = (bay.shelves || 0) + 1;
                                  const baseW = bayW - 4;
                                  const baseH = bayH - 4;
                                  const elements = [];

                                  const vXs = [bayX + 2];
                                  for (let vIdx = 0; vIdx < (bay.verticalShelves || 0); vIdx++) {
                                      vXs.push(getVerticalShelfX(bay, vIdx, baseW, bayX));
                                  }
                                  vXs.push(bayX + bayW - 2);

                                  const hYs = [bayY + 2];
                                  for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
                                      hYs.push(getShelfY(bay, sIdx, baseH, bayY));
                                  }
                                  hYs.push(bayY + bayH - 2);

                                  // Horizontal segments
                                  for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
                                    const sY = hYs[sIdx + 1];
                                    for (let cIdx = 0; cIdx < cols; cIdx++) {
                                      const pId = \`h-\${sIdx}-\${cIdx}\`;
                                      const isRemoved = (bay.removedPartitions || []).includes(pId);
                                      const sX1 = vXs[cIdx];
                                      const sX2 = vXs[cIdx + 1];
                                      elements.push(
                                        <g key={pId} 
                                          className={isFullScreenDrawing ? (dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity") : ""} 
                                          onPointerDown={(e) => {
                                              if (!isFullScreenDrawing) return;
                                              setDragState({
                                                  bayIdx: idx, type: 'h', idx: sIdx, startX: e.clientX, startY: e.clientY,
                                                  bayX, bayY, bayW, bayH, isDragging: false, partitionId: pId
                                              });
                                              e.stopPropagation();
                                          }}
                                        >
                                          {isFullScreenDrawing && <line x1={sX1} y1={sY} x2={sX2} y2={sY} stroke="transparent" strokeWidth="15" />}
                                          <line
                                            x1={sX1} y1={sY} x2={sX2} y2={sY}
                                            stroke={isRemoved ? (isFullScreenDrawing ? "rgba(71,85,105,0.3)" : "transparent") : "#475569"}
                                            strokeWidth={isRemoved ? "1" : "2"}
                                            strokeDasharray={isRemoved ? "4,4" : "none"}
                                          />
                                        </g>
                                      );
                                    }
                                  }

                                  // Vertical segments
                                  for (let vIdx = 0; vIdx < (bay.verticalShelves || 0); vIdx++) {
                                    const vX = vXs[vIdx + 1];
                                    for (let rIdx = 0; rIdx < rows; rIdx++) {
                                      const pId = \`v-\${vIdx}-\${rIdx}\`;
                                      const isRemoved = (bay.removedPartitions || []).includes(pId);
                                      const vY1 = hYs[rIdx];
                                      const vY2 = hYs[rIdx + 1];
                                      elements.push(
                                        <g key={pId} 
                                          className={isFullScreenDrawing ? (dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity") : ""} 
                                          onPointerDown={(e) => {
                                              if (!isFullScreenDrawing) return;
                                              setDragState({
                                                  bayIdx: idx, type: 'v', idx: vIdx, startX: e.clientX, startY: e.clientY,
                                                  bayX, bayY, bayW, bayH, isDragging: false, partitionId: pId
                                              });
                                              e.stopPropagation();
                                          }}
                                        >
                                          {isFullScreenDrawing && <line x1={vX} y1={vY1} x2={vX} y2={vY2} stroke="transparent" strokeWidth="15" />}
                                          <line
                                            x1={vX} y1={vY1} x2={vX} y2={vY2}
                                            stroke={isRemoved ? (isFullScreenDrawing ? "rgba(71,85,105,0.3)" : "transparent") : "#475569"}
                                            strokeWidth={isRemoved ? "1" : "2"}
                                            strokeDasharray={isRemoved ? "4,4" : "none"}
                                          />
                                        </g>
                                      );
                                    }
                                  }

                                  return elements;
                                })()}`;

content = content.replace(oldOpenSvgRegex, newOpenSvg);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated SVG dragging logic!");
