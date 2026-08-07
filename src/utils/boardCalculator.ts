export interface BoardPiece {
  w: number;
  l: number;
  qty: number;
}

class Bin {
  width: number;
  height: number;
  freeRectangles: { x: number; y: number; w: number; h: number }[];

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
    this.freeRectangles = [{ x: 0, y: 0, w: width, h: height }];
  }

  insert(w: number, h: number): boolean {
    for (let i = 0; i < this.freeRectangles.length; i++) {
      const rect = this.freeRectangles[i];
      if (rect.w >= w && rect.h >= h) {
        // Fits!
        this.split(i, w, h);
        return true;
      }
      // Try rotated
      if (rect.w >= h && rect.h >= w) {
        this.split(i, h, w);
        return true;
      }
    }
    return false;
  }

  private split(rectIndex: number, w: number, h: number) {
    const rect = this.freeRectangles[rectIndex];
    this.freeRectangles.splice(rectIndex, 1);

    // Guillotine split
    // Split horizontally or vertically depending on remaining space
    const r1 = { x: rect.x + w, y: rect.y, w: rect.w - w, h: h };
    const r2 = { x: rect.x, y: rect.y + h, w: rect.w, h: rect.h - h };
    
    // Sort so smaller free rectangles are pushed back or handled
    if (r1.w > 0 && r1.h > 0) this.freeRectangles.push(r1);
    if (r2.w > 0 && r2.h > 0) this.freeRectangles.push(r2);
    
    // Sort free rectangles by area descending to fit larger items first? 
    // Actually, smaller first (Best Fit) or larger first? Let's just keep it simple.
  }
}

export function calculateRequiredBoards(pieces: BoardPiece[], boardW = 1220, boardL = 2440): number {
  const allPieces: { w: number; h: number }[] = [];
  pieces.forEach(p => {
    for (let i = 0; i < p.qty; i++) {
      allPieces.push({ w: Math.max(p.w, p.l), h: Math.min(p.w, p.l) });
    }
  });

  // Sort pieces by area descending, then longest edge
  allPieces.sort((a, b) => {
    const areaA = a.w * a.h;
    const areaB = b.w * b.h;
    if (areaB !== areaA) return areaB - areaA;
    return b.w - a.w;
  });

  const bins: Bin[] = [];

  for (const piece of allPieces) {
    let placed = false;
    for (const bin of bins) {
      if (bin.insert(piece.w, piece.h)) {
        placed = true;
        break;
      }
    }
    if (!placed) {
      const newBin = new Bin(Math.max(boardW, boardL), Math.min(boardW, boardL));
      if (!newBin.insert(piece.w, piece.h)) {
          // If the piece is larger than the board itself, we have to count it as taking a full board
          // (or it's an error, but let's just create a board for it)
      }
      bins.push(newBin);
    }
  }

  return bins.length;
}
