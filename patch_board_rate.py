import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

getBoardRateNew = """export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number,
  quality: string,
): number => {
  if (boardId === "crca_powder_coated" || boardId === "ss_304") {
    return baseRate * (thickness / 1.2);
  }
"""

content = re.sub(
    r'export const getBoardRate = \(\n  boardId: string,\n  baseRate: number,\n  thickness: number,\n  quality: string,\n\): number => \{\n',
    getBoardRateNew,
    content
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
