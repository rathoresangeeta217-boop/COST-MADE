const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// 1. Add removedPartitions to ColumnConfig
content = content.replace(
  /boxShutters\?: boolean\[\];/,
  `boxShutters?: boolean[];\n  removedPartitions?: string[];`
);

// 2. Update toggleDoor to also handle partitions
content = content.replace(
  /const toggleDoor = \(doorId: string\) => \{/,
  `const togglePartition = (partitionId: string, bayIdx: number) => {
    const newBays = [...bays];
    const bay = newBays[bayIdx];
    const removed = new Set(bay.removedPartitions || []);
    if (removed.has(partitionId)) {
      removed.delete(partitionId);
    } else {
      removed.add(partitionId);
    }
    bay.removedPartitions = Array.from(removed);
    setBays(newBays);
  };

  const toggleDoor = (doorId: string) => {`
);

// 3. Update the SVG rendering for "open" shelves
const oldOpenSvg = `{/* Draw horizontal open shelves */}
                                {Array.from({ length: bay.shelves }).map((_, sIdx) => {
                                  const sY = bayY + ((sIdx + 1) * bayH) / (bay.shelves + 1);
                                  return (
                                    <line
                                      key={sIdx}
                                      x1={bayX + 2}
                                      y1={sY}
                                      x2={bayX + bayW - 2}
                                      y2={sY}
                                      stroke="#475569"
                                      strokeWidth="2"
                                    />
                                  );
                                })}
                                {/* Draw vertical shelves (dividers) */}
                                {bay.verticalShelves && bay.verticalShelves > 0 ? Array.from({ length: bay.verticalShelves }).map((_, vIdx) => {
                                  const vX = bayX + ((vIdx + 1) * bayW) / (bay.verticalShelves! + 1);
                                  return (
                                    <line
                                      key={\`v-\${vIdx}\`}
                                      x1={vX}
                                      y1={bayY + 2}
                                      x2={vX}
                                      y2={bayY + bayH - 2}
                                      stroke="#475569"
                                      strokeWidth="2"
                                    />
                                  );
                                }) : null}`;

const newOpenSvg = `{/* Draw horizontal open shelves (segmented) */}
                                {(() => {
                                  const cols = (bay.verticalShelves || 0) + 1;
                                  const rows = (bay.shelves || 0) + 1;
                                  const cellW = (bayW - 4) / cols;
                                  const cellH = (bayH - 4) / rows;
                                  const elements = [];

                                  // Horizontal segments
                                  for (let sIdx = 0; sIdx < (bay.shelves || 0); sIdx++) {
                                    for (let cIdx = 0; cIdx < cols; cIdx++) {
                                      const pId = \`h-\${sIdx}-\${cIdx}\`;
                                      const isRemoved = (bay.removedPartitions || []).includes(pId);
                                      const sY = bayY + 2 + (sIdx + 1) * cellH;
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
                                      const vY = bayY + 2 + rIdx * cellH;
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

content = content.replace(oldOpenSvg, newOpenSvg);

// 4. Update total calculation for horizontal and vertical shelves
const oldTotalShelves = `totalShelvesCount += bay.shelves;
        if (bay.verticalShelves) totalVerticalShelvesCount += bay.verticalShelves;`;

const newTotalShelves = `
        const cols = (bay.verticalShelves || 0) + 1;
        const rows = (bay.shelves || 0) + 1;
        let removedH = 0;
        let removedV = 0;
        (bay.removedPartitions || []).forEach(p => {
          if (p.startsWith('h-')) removedH++;
          if (p.startsWith('v-')) removedV++;
        });
        totalShelvesCount += bay.shelves - (removedH / cols);
        if (bay.verticalShelves) totalVerticalShelvesCount += bay.verticalShelves - (removedV / rows);`;

content = content.replace(oldTotalShelves, newTotalShelves);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated!");
