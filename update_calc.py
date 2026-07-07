import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

calc_old = """    // Vertical Partitions
    const numPartitions = numBays - 1;
    if (numPartitions > 0) {
      pieces.push({
        label: "Vertical Partitions",
        w: depth - 20,
        l: sideH,
        qty: numPartitions,
        ebMm: sideH * numPartitions,
      });
    }

    // Inside dimensions for columns
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    const bayWidth = Math.max(0, (innerWidth - totalPartitionThickness) / numBays);

    // Horizontal Partitions
    const numHPartitions = numRows - 1;
    if (numHPartitions > 0) {
      pieces.push({
        label: "Horizontal Partitions",
        w: bayWidth,
        l: depth - 20,
        qty: numHPartitions * numBays,
        ebMm: bayWidth * numHPartitions * numBays,
      });
    }
    const totalHPartitionThickness = numHPartitions * thickness;
    const baySideH = Math.max(0, (sideH - totalHPartitionThickness) / numRows);"""

calc_new = """    // Helpers for offsets
    const getColOffset = (idx: number, total: number) => colOffsets[idx] ?? ((idx + 1) / total);
    const getRowOffset = (idx: number, total: number) => rowOffsets[idx] ?? ((idx + 1) / total);
    
    // Inside dimensions for columns
    const numPartitions = numBays - 1;
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    
    const numHPartitions = numRows - 1;
    const totalHPartitionThickness = numHPartitions * thickness;

    // Helper to get bayWidth
    const getColWidth = (c: number) => {
        const prevOffset = c > 0 ? getColOffset(c - 1, numBays) : 0;
        const nextOffset = c < numBays - 1 ? getColOffset(c, numBays) : 1;
        const span = nextOffset - prevOffset;
        return Math.max(0, (innerWidth - totalPartitionThickness) * span);
    };

    // Helper to get baySideH
    const getRowHeight = (r: number) => {
        const prevOffset = r > 0 ? getRowOffset(r - 1, numRows) : 0;
        const nextOffset = r < numRows - 1 ? getRowOffset(r, numRows) : 1;
        const span = nextOffset - prevOffset;
        return Math.max(0, (sideH - totalHPartitionThickness) * span);
    };

    // Vertical Partitions
    if (numPartitions > 0) {
      pieces.push({
        label: "Vertical Partitions",
        w: depth - 20,
        l: sideH,
        qty: numPartitions,
        ebMm: sideH * numPartitions,
      });
    }

    // Horizontal Partitions
    if (numHPartitions > 0) {
      for (let c = 0; c < numBays; c++) {
        const w = getColWidth(c);
        if (w > 0) {
            pieces.push({
                label: `Horizontal Partitions (Col ${c + 1})`,
                w: w,
                l: depth - 20,
                qty: numHPartitions,
                ebMm: w * numHPartitions,
            });
        }
      }
    }
    
    // Legacy single bay values (avg) for UI display
    const bayWidth = Math.max(0, (innerWidth - totalPartitionThickness) / numBays);
    const baySideH = Math.max(0, (sideH - totalHPartitionThickness) / numRows);"""

content = content.replace(calc_old, calc_new)

# Inside bays.forEach, we need to redefine bayWidth and baySideH
content = content.replace(
    'bays.forEach((bay, index) => {',
    'bays.forEach((bay, index) => {\n      const r = Math.floor(index / numBays);\n      const c = index % numBays;\n      const bayWidth = getColWidth(c);\n      const baySideH = getRowHeight(r);'
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
