import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_block = """    // Dividers / Vertical Partitions
    const numPartitions = numBays - 1;
    if (numPartitions > 0) {
      pieces.push({
        label: "Vertical Partitions",
        w: depth - 20,
        l: baySideH,
        qty: numPartitions,
        ebMm: sideH * numPartitions, // front edges
      });
    }

    // Inside dimensions for columns
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    const bayWidth = Math.max(0, (innerWidth - totalPartitionThickness) / numBays);"""

new_block = """    // Dividers / Vertical Partitions
    const isHoriz = bayDirection === 'horizontal';
    const numPartitions = numBays - 1;
    if (numPartitions > 0) {
      pieces.push({
        label: isHoriz ? "Horizontal Partitions" : "Vertical Partitions",
        w: depth - 20,
        l: isHoriz ? (width - thickness * 2) : sideH,
        qty: numPartitions,
        ebMm: (isHoriz ? (width - thickness * 2) : sideH) * numPartitions,
      });
    }

    // Inside dimensions for columns
    const innerWidth = Math.max(0, width - thickness * 2);
    const totalPartitionThickness = numPartitions * thickness;
    const baySideH = isHoriz ? Math.max(0, (sideH - totalPartitionThickness) / numBays) : sideH;
    const bayWidth = isHoriz ? innerWidth : Math.max(0, (innerWidth - totalPartitionThickness) / numBays);"""

content = content.replace(old_block, new_block)

# Also fix line 496: pieces.push({ label: "Side Panels", w: depth, l: baySideH, qty: 2, ebMm: (sideH * 2 + depth) * 2 });
# It should use sideH
content = content.replace('pieces.push({ label: "Side Panels", w: depth, l: baySideH, qty: 2, ebMm: (sideH * 2 + depth) * 2 });', 'pieces.push({ label: "Side Panels", w: depth, l: sideH, qty: 2, ebMm: (sideH * 2 + depth) * 2 });')

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
