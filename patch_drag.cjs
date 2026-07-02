const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const dragLogic = `
                  onPointerMove={(e) => {
                    if (!dragState) return;
                    e.preventDefault();
                    
                    const { bayIdx, type, idx, startX, startY, bayW, bayH, partitionId } = dragState;
                    
                    // Simple drag calculation (assume 1px move = 1 unit for now, need scale if zoomed)
                    const dx = e.clientX - startX;
                    const dy = e.clientY - startY;
                    
                    if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
                        if (!dragState.isDragging) {
                           setDragState({...dragState, isDragging: true});
                        }
                    }

                    if (!dragState.isDragging) return;

                    const bay = bays[bayIdx];
                    const scale = (isFullScreenDrawing ? zoomLevel : 1) * 0.4; // approx SVG scale
                    
                    if (type === 'h') {
                        // horizontal partition
                        let hPositions = bay.shelfHeights || {};
                        let currentRelY = 0;
                        if (hPositions[idx] !== undefined) {
                            currentRelY = hPositions[idx];
                        } else {
                            currentRelY = (bayH / ((bay.shelves || 0) + 1)) * (idx + 1);
                        }
                        
                        let newY = currentRelY + (dy / scale);
                        newY = Math.max(10, Math.min(bayH - 10, newY)); // clamp
                        
                        updateBay(bayIdx, {
                            shelfHeights: { ...hPositions, [idx]: newY }
                        });
                        setDragState({...dragState, startY: e.clientY}); // reset start for relative drag
                    } else if (type === 'v') {
                         let vPositions = bay.verticalShelfPositions || {};
                         let currentRelX = 0;
                         if (vPositions[idx] !== undefined) {
                            currentRelX = vPositions[idx];
                         } else {
                            currentRelX = (bayW / ((bay.verticalShelves || 0) + 1)) * (idx + 1);
                         }
                         
                         let newX = currentRelX + (dx / scale);
                         newX = Math.max(10, Math.min(bayW - 10, newX));
                         
                         updateBay(bayIdx, {
                             verticalShelfPositions: { ...vPositions, [idx]: newX }
                         });
                         setDragState({...dragState, startX: e.clientX});
                    }
                  }}
                  onPointerUp={(e) => {
                    if (dragState) {
                       setDragState(null);
                    }
                  }}
                  onPointerLeave={(e) => {
                    if (dragState) {
                       setDragState(null);
                    }
                  }}
`;

content = content.replace(/xmlns="http:\/\/www\.w3\.org\/2000\/svg"/, 'xmlns="http://www.w3.org/2000/svg"' + dragLogic);
fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Added pointer drag logic");
