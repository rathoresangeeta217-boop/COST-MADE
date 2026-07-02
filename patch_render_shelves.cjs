const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// 1. Inject renderShelves helper after togglePartition
const renderShelvesHelper = `
  const renderShelves = (bay: ColumnConfig, idx: number, bayX: number, bayY: number, bayW: number, bayH: number) => {
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
                if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                e.stopPropagation();
            }}
            onClick={(e) => e.stopPropagation()}
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
                if (e.target && (e.target as Element).setPointerCapture) (e.target as Element).setPointerCapture(e.pointerId);
                e.stopPropagation();
            }}
            onClick={(e) => e.stopPropagation()}
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
  };
`;

content = content.replace(
  /const togglePartition = \(partitionId: string, bayIdx: number\) => \{/,
  renderShelvesHelper + '\n  const togglePartition = (partitionId: string, bayIdx: number) => {'
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Injected renderShelves helper");
