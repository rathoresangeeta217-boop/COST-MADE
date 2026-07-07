import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# State variables
content = content.replace(
    'const [numBays, setNumBays] = useState<number>(3);',
    'const [numBays, setNumBays] = useState<number>(3);\n  const [colOffsets, setColOffsets] = useState<Record<number, number>>({});\n  const [rowOffsets, setRowOffsets] = useState<Record<number, number>>({});'
)

# Project saving
content = content.replace(
    "boardThickness, innerMica, outerMica, numBays, numRows, supportLegsCount,",
    "boardThickness, innerMica, outerMica, numBays, numRows, colOffsets, rowOffsets, supportLegsCount,"
)

# Project loading
content = content.replace(
    "if (c.numRows) setNumRows(c.numRows);",
    "if (c.numRows) setNumRows(c.numRows);\n      if (c.colOffsets) setColOffsets(c.colOffsets);\n      if (c.rowOffsets) setRowOffsets(c.rowOffsets);"
)

# dependencies of calcData
content = content.replace(
    "quality, numBays, numRows, supportLegsCount, bays, showAdvancedMaterials, pieceOverrides, thicknessOverrides, innerMica, outerMica]);",
    "quality, numBays, numRows, colOffsets, rowOffsets, supportLegsCount, bays, showAdvancedMaterials, pieceOverrides, thicknessOverrides, innerMica, outerMica]);"
)

# dependencies of calcData drawer
content = content.replace(
    "boardThickness, drawerWidth, drawerDepth, drawerHeight, quality, numBays, numRows, supportLegsCount, bays]",
    "boardThickness, drawerWidth, drawerDepth, drawerHeight, quality, numBays, numRows, colOffsets, rowOffsets, supportLegsCount, bays]"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
