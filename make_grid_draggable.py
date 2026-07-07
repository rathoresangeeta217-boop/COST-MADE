import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Update drag logic
old_drag_logic = """                    if (type === 'h') {
                        let hPositions = bay.shelfOffsets || {};
                        let currentRel = hPositions[idx];
                        if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.shelves || 0) + 1);
                        }
                        
                        let deltaRel = (dy * scale) / bayH;
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));
                        
                        updateBay(bayIdx, {
                            shelfOffsets: { ...hPositions, [idx]: newRel }
                        });
                        setDragState({...dragState, startY: e.clientY}); 
                    } else if (type === 'v') {
                         let vPositions = bay.verticalShelfOffsets || {};
                         let currentRel = vPositions[idx];
                         if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.verticalShelves || 0) + 1);
                         }
                         
                         let deltaRel = (dx * scale) / bayW;
                         let newRel = currentRel + deltaRel;
                         newRel = Math.max(0.05, Math.min(0.95, newRel));
                         
                         updateBay(bayIdx, {
                             verticalShelfOffsets: { ...vPositions, [idx]: newRel }
                         });
                         setDragState({...dragState, startX: e.clientX});
                    }"""

new_drag_logic = """                    if (type === 'h') {
                        if (bayH === undefined) return;
                        let hPositions = bay.shelfOffsets || {};
                        let currentRel = hPositions[idx];
                        if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.shelves || 0) + 1);
                        }
                        
                        let deltaRel = (dy * scale) / bayH;
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));
                        
                        updateBay(bayIdx, {
                            shelfOffsets: { ...hPositions, [idx]: newRel }
                        });
                        setDragState({...dragState, startY: e.clientY}); 
                    } else if (type === 'v') {
                         if (bayW === undefined) return;
                         let vPositions = bay.verticalShelfOffsets || {};
                         let currentRel = vPositions[idx];
                         if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.verticalShelves || 0) + 1);
                         }
                         
                         let deltaRel = (dx * scale) / bayW;
                         let newRel = currentRel + deltaRel;
                         newRel = Math.max(0.05, Math.min(0.95, newRel));
                         
                         updateBay(bayIdx, {
                             verticalShelfOffsets: { ...vPositions, [idx]: newRel }
                         });
                         setDragState({...dragState, startX: e.clientX});
                    } else if (type === 'main_v') {
                        let currentRel = colOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numBays;
                        }
                        let deltaRel = (dx * scale) / (width - 16); // Total drawW without padding is roughly width
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));
                        setColOffsets(prev => ({ ...prev, [idx]: newRel }));
                        setDragState({...dragState, startX: e.clientX});
                    } else if (type === 'main_h') {
                        let currentRel = rowOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numRows;
                        }
                        let deltaRel = (dy * scale) / (height - 16); // Total drawH without padding is roughly height
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));
                        setRowOffsets(prev => ({ ...prev, [idx]: newRel }));
                        setDragState({...dragState, startY: e.clientY});
                    }"""

content = content.replace(old_drag_logic, new_drag_logic)

# Replace Grid Dividers SVG portion
old_svg_grid = """                      {/* Grid Dividers */}
                      {Array.from({ length: numBays - 1 }).map((_, cIdx) => {
                         const bayW = (drawW - 16) / numBays;
                         const x = paddingX + 8 + (cIdx + 1) * bayW;
                         return <line key={`vdiv-${cIdx}`} x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke="#475569" strokeWidth="2.5" />;
                      })}
                      {Array.from({ length: numRows - 1 }).map((_, rIdx) => {
                         const bayH = (drawH - 16) / numRows;
                         const y = paddingY + 8 + (rIdx + 1) * bayH;
                         return <line key={`hdiv-${rIdx}`} x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke="#475569" strokeWidth="2.5" />;
                      })}"""

new_svg_grid = """                      {/* Grid Dividers */}
                      {Array.from({ length: numBays - 1 }).map((_, cIdx) => {
                         const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                         const x = paddingX + 8 + getColOffset(cIdx, numBays) * (drawW - 16);
                         const isDragging = dragState?.type === 'main_v' && dragState.idx === cIdx;
                         return (
                            <g key={`vdiv-${cIdx}`}
                               className={isDragging ? "cursor-grabbing" : "cursor-col-resize hover:opacity-80 transition-opacity"}
                               onPointerDown={(e) => {
                                  setDragState({ bayIdx: -1, type: 'main_v', idx: cIdx, startX: e.clientX, startY: e.clientY, isDragging: false });
                                  if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                                  e.stopPropagation();
                               }}
                            >
                                <line x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke="transparent" strokeWidth="15" />
                                <line x1={x} y1={paddingY + 8} x2={x} y2={paddingY + drawH - 8} stroke={isDragging ? "#6366f1" : "#475569"} strokeWidth="2.5" />
                            </g>
                         );
                      })}
                      {Array.from({ length: numRows - 1 }).map((_, rIdx) => {
                         const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                         const y = paddingY + 8 + getRowOffset(rIdx, numRows) * (drawH - 16);
                         const isDragging = dragState?.type === 'main_h' && dragState.idx === rIdx;
                         return (
                            <g key={`hdiv-${rIdx}`}
                               className={isDragging ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"}
                               onPointerDown={(e) => {
                                  setDragState({ bayIdx: -1, type: 'main_h', idx: rIdx, startX: e.clientX, startY: e.clientY, isDragging: false });
                                  if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                                  e.stopPropagation();
                               }}
                            >
                                <line x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke="transparent" strokeWidth="15" />
                                <line x1={paddingX + 8} y1={y} x2={paddingX + drawW - 8} y2={y} stroke={isDragging ? "#6366f1" : "#475569"} strokeWidth="2.5" />
                            </g>
                         );
                      })}"""

content = content.replace(old_svg_grid, new_svg_grid)

# We also need to update the `bayX`, `bayY`, `bayW`, `bayH` in the bays.map
# Instead of assuming uniform width, it should use the actual offsets
old_bays_map_vars = """                      {/* Draw column/row dividers and styles */}
                      {bays.map((bay, idx) => {
                        const r = Math.floor(idx / numBays);
                        const c = idx % numBays;
                        const bayW = (drawW - 16) / numBays;
                        const bayH = (drawH - 16) / numRows;
                        const bayX = paddingX + 8 + c * bayW;
                        const bayY = paddingY + 8 + r * bayH;"""

new_bays_map_vars = """                      {/* Draw column/row dividers and styles */}
                      {bays.map((bay, idx) => {
                        const r = Math.floor(idx / numBays);
                        const c = idx % numBays;
                        
                        const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
                        const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
                        
                        const colStart = c > 0 ? getColOffset(c - 1, numBays) : 0;
                        const colEnd = c < numBays - 1 ? getColOffset(c, numBays) : 1;
                        const rowStart = r > 0 ? getRowOffset(r - 1, numRows) : 0;
                        const rowEnd = r < numRows - 1 ? getRowOffset(r, numRows) : 1;
                        
                        const bayW = (colEnd - colStart) * (drawW - 16);
                        const bayH = (rowEnd - rowStart) * (drawH - 16);
                        const bayX = paddingX + 8 + colStart * (drawW - 16);
                        const bayY = paddingY + 8 + rowStart * (drawH - 16);"""

content = content.replace(old_bays_map_vars, new_bays_map_vars)


# Replace type DragState = ...
# It might not be defined explicitly if it's inline, let's find `useState<any>(null)`
content = content.replace(
    'const [dragState, setDragState] = useState<any>(null);',
    'const [dragState, setDragState] = useState<any>(null);' # We'll just leave it as any
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
