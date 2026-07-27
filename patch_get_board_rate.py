import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_func = """export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number,
  quality: string,
): number => {
    if (boardId === "crca_powder_coated") {"""

new_func = """export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number,
  quality: string,
): number => {
    console.log(`getBoardRate called with boardId: ${boardId}, baseRate: ${baseRate}, thickness: ${thickness}, quality: ${quality}`);
    if (boardId === "crca_powder_coated") {"""

content = content.replace(old_func, new_func)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
