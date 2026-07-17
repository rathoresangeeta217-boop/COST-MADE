import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

metal_logic = """
    const pieces: {
      label: string;
      w: number;
      l: number;
      qty: number;
      customCostPerSqFt?: number;
      ebMm?: number;
    }[] = [];

    let totalHardwareCost = 0;
    let totalLaborCost = BASE_LABOR_COST + (numBays * LABOR_PER_BAY_COST);
    let totalSolidShuttersCount = 0;
    let totalGlassShuttersCount = 0;
    let totalDrawersCount = 0;
    let totalHingesCount = 0;
    let totalHandlesCount = 0;
    let totalIndividualLocksCount = 0;
    let totalCentralLocksCount = 0;
    let totalShelvesCount = 0;
    let totalVerticalShelvesCount = 0;
    let totalHalfShelvesCount = 0;

    if (constructionCategory === "metal") {
      const activeMetalBoard = boards.find(x => x.id === boardId) || boards[0];
      const angleRate = getBoardRate(activeMetalBoard.id, activeMetalBoard.costPerSqFt, angleThickness, quality);

      const numVertAngles = addVerticalPartitionMiddle ? 6 : 4;
      pieces.push({ label: `Slotted Angle ${angleThickness}mm (${activeMetalBoard.name})`, w: 100, l: height, qty: numVertAngles, customCostPerSqFt: angleRate });

      const numShelves = numRows + 1;
      let shelfCostSqFt = 0;
      let shelfLabel = "";

      if (shelfMaterialType === "metal") {
        shelfCostSqFt = getBoardRate(activeMetalBoard.id, activeMetalBoard.costPerSqFt, boardThickness, quality);
        shelfLabel = `Metal Shelf ${boardThickness}mm (${activeMetalBoard.name})`;
      } else {
        const activeWoodenBoard = boards.find(x => x.id === woodenShelfId) || boards[0];
        shelfCostSqFt = getBoardRate(activeWoodenBoard.id, activeWoodenBoard.costPerSqFt, woodenShelfThickness, quality);
        shelfLabel = `Wooden Shelf ${woodenShelfThickness}mm (${activeWoodenBoard.name})`;
      }

      if (addVerticalPartitionMiddle) {
        pieces.push({ label: `Vertical Partition Middle (${shelfMaterialType})`, w: depth, l: height, qty: 1, customCostPerSqFt: shelfCostSqFt });
        pieces.push({ label: shelfLabel, w: width / 2, l: depth, qty: numShelves * 2, customCostPerSqFt: shelfCostSqFt });
      } else {
        pieces.push({ label: shelfLabel, w: width, l: depth, qty: numShelves, customCostPerSqFt: shelfCostSqFt });
      }
      
      // Hardware: corner plates, nuts/bolts
      totalHardwareCost = 300 + (numShelves * 50); // rough estimate for metal racks
    } else {
      // Outer shell
"""

# We need to find the exact place to replace.
# In src/pages/CustomStorageCalculator.tsx:
# const pieces: { ... }[] = [];
# // Outer shell

content = re.sub(
    r'    const pieces: \{\n      label: string;\n      w: number;\n      l: number;\n      qty: number;\n      customCostPerSqFt\?: number;\n      ebMm\?: number;\n    \}\[\] = \[\];\n\n    // Outer shell',
    metal_logic,
    content
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
