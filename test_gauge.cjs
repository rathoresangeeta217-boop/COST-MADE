const getBoardRate = (
  boardId,
  baseRate,
  thickness,
  quality,
) => {
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
  }
  return 0;
}
console.log(getBoardRate("crca_powder_coated", 150, 1.6, "standard"));
console.log(getBoardRate("crca_powder_coated", 150, 0.8, "standard"));
