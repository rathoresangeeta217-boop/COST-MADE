const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const old1DrawerOpenSvg = `{/* Render open adjustable shelves inside remaining space below drawer */}
                                      {Array.from({ length: bay.shelves }).map((_, sIdx) => {
                                        const remainingH = bayH - dH;
                                        const sY = dY + dH + ((sIdx + 1) * remainingH) / (bay.shelves + 1);
                                        return (
                                          <line
                                            key={sIdx}
                                            x1={bayX + 3}
                                            y1={sY}
                                            x2={bayX + bayW - 3}
                                            y2={sY}
                                            stroke="#475569"
                                            strokeWidth="1.5"
                                          />
                                        );
                                      })}
                                      {/* Visible vertical dividers below drawer */}
                                      {bay.verticalShelves && bay.verticalShelves > 0 ? Array.from({ length: bay.verticalShelves }).map((_, vIdx) => {
                                        const vX = bayX + ((vIdx + 1) * bayW) / (bay.verticalShelves! + 1);
                                        return (
                                          <line
                                            key={\`v-\${vIdx}\`}
                                            x1={vX}
                                            y1={dY + dH + 2}
                                            x2={vX}
                                            y2={bayY + bayH - 2}
                                            stroke="#475569"
                                            strokeWidth="1.5"
                                          />
                                        );
                                      }) : null}`;

const new1DrawerOpenSvg = `{/* Render open adjustable shelves inside remaining space below drawer (segmented) */}
                                      {(() => {
                                        const remainingH = bayH - dH;
                                        const cols = (bay.verticalShelves || 0) + 1;
                                        const rows = (bay.shelves || 0) + 1;
                                        const cellW = (bayW - 4) / cols;
                                        const cellH = remainingH / rows;
                                        const elements = [];

                                        // Horizontal segments
                                        for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
                                          for (let cIdx = 0; cIdx < cols; cIdx++) {
                                            const pId = \`h-\${sIdx}-\${cIdx}\`;
                                            const isRemoved = (bay.removedPartitions || []).includes(pId);
                                            const sY = dY + dH + (sIdx + 1) * cellH;
                                            const sX = bayX + 2 + cIdx * cellW;
                                            elements.push(
                                              <g key={pId} 
                                                className={isFullScreenDrawing ? "cursor-pointer hover:opacity-80 transition-opacity" : ""} 
                                                onClick={() => isFullScreenDrawing && togglePartition(pId, idx)}
                                              >
                                                {isFullScreenDrawing && <line x1={sX} y1={sY} x2={sX + cellW} y2={sY} stroke="transparent" strokeWidth="15" />}
                                                <line
                                                  x1={sX} y1={sY} x2={sX + cellW} y2={sY}
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
                                          for (let rIdx = 0; rIdx < rows; rIdx++) {
                                            const pId = \`v-\${vIdx}-\${rIdx}\`;
                                            const isRemoved = (bay.removedPartitions || []).includes(pId);
                                            const vX = bayX + 2 + (vIdx + 1) * cellW;
                                            const vY = dY + dH + rIdx * cellH;
                                            elements.push(
                                              <g key={pId} 
                                                className={isFullScreenDrawing ? "cursor-pointer hover:opacity-80 transition-opacity" : ""} 
                                                onClick={() => isFullScreenDrawing && togglePartition(pId, idx)}
                                              >
                                                {isFullScreenDrawing && <line x1={vX} y1={vY} x2={vX} y2={vY + cellH} stroke="transparent" strokeWidth="15" />}
                                                <line
                                                  x1={vX} y1={vY} x2={vX} y2={vY + cellH}
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

if (content.includes(old1DrawerOpenSvg)) {
  content = content.replace(old1DrawerOpenSvg, new1DrawerOpenSvg);
  fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
  console.log("Updated 1_drawer_open shelves!");
} else {
  console.log("Could not find old SVG for 1_drawer_open");
}
