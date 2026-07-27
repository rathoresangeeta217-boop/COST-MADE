import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_func = """export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number,
  quality: string,
): number => {
    console.log(`getBoardRate called with boardId: ${boardId}, baseRate: ${baseRate}, thickness: ${thickness}, quality: ${quality}`);
    if (boardId === "crca_powder_coated") {
    switch (thickness) {
      case 2: return 125;
      case 1.6: return 96;
      case 1.2: return 72;
      case 1: return 62;
      case 0.8: return 52;
      case 0.6: return 41;
      default: return baseRate * (thickness / 1.2);
    }
  }"""

new_func = """export const getBoardRate = (
  boardId: string,
  baseRate: number,
  thickness: number | string,
  quality: string,
): number => {
    const numThk = Number(thickness);
    if (boardId === "crca_powder_coated") {
    if (numThk === 2) return 125;
    if (numThk === 1.6) return 96;
    if (numThk === 1.2) return 72;
    if (numThk === 1) return 62;
    if (numThk === 0.8) return 52;
    if (numThk === 0.6) return 41;
    return baseRate * (numThk / 1.2);
  }"""

content = content.replace(old_func, new_func)
with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
