const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const dragLogic = `
                  onPointerMove={(e) => {
                    if (!dragState) return;
                    e.preventDefault();
                    
                    const { bayIdx, type, idx, startX, startY, bayW, bayH, partitionId } = dragState;
                    
                    // Simple drag calculation
                    const dx = e.clientX - startX;
                    const dy = e.clientY - startY;
                    
                    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
                        if (!dragState.isDragging) {
                           setDragState({...dragState, isDragging: true});
                        }
                    }

                    if (!dragState.isDragging) return;

                    const bay = bays[bayIdx];
                    // The SVG scales differently depending on full screen and zoom
                    // The easiest way is to use SVG's client rect to calculate ratio, but let's approximate:
                    // SVG is drawn at width={(width+100)*0.4*zoomLevel} (if full screen), but its viewBox is (width+100)
                    // So scaling factor from DOM pixels to SVG coordinates is roughly:
                    // scale = viewBox_width / dom_width = (width+100) / ((width+100)*0.4*zoom) = 1 / (0.4 * zoom)
                    const scale = 1 / (0.4 * (isFullScreenDrawing ? zoomLevel : 1));
                    
                    if (type === 'h') {
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
