import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_func = """export const getBoardRate = (
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
  }
  if (boardId === "ss_304") {
    return baseRate * (thickness / 1.2);
  }
  if (quality === "affordable") {
    if (boardId === "plpb") {
      if (thickness === 11) return 27;
      if (thickness === 17) return 29;
      if (thickness === 18) return 34;
      if (thickness === 25) return 42;
    }
    if (boardId === "hdhmr") {
      if (Math.abs(thickness - 16.75) < 0.1) return 88;
      if (thickness === 18) return 99;
      if (thickness === 25) return 135;
    }
    if (boardId === "ply_laminate") {
      if (thickness === 6) return 22;
      if (thickness === 9) return 35;
      if (thickness === 12) return 38;
      if (thickness === 15) return 46;
      if (thickness === 16) return 46;
      if (thickness === 18) return 55;
    }
    if (boardId === "mdf") {
      if (thickness === 17) return 55;
      if (thickness === 18) return 60;
      if (thickness === 25) return 80;
      if (thickness === 35) return 112;
    }
  } else {
    // Standard quality logic
    if (boardId === "plpb") {
      if (thickness === 18) return 49;
      if (thickness === 25) return 63;
      if (thickness === 36) return 98;
    }
    if (boardId === "hdhmr") {
      if (thickness === 25) return 108;
    }
    if (boardId === "mdf") {
      if (thickness === 18) return 61;
      if (thickness === 25) return 83;
      if (thickness === 36) return 122;
    }
    if (boardId === "bwr_plywood") {
      if (thickness === 18) return 74;
    }
    if (boardId === "bwp_plywood") {
      if (thickness === 18) return 110;
    }
  }
  
  // Default fallback scaling
  return baseRate * (thickness / 18);
};"""

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
  }
  if (boardId === "ss_304") {
    return baseRate * (numThk / 1.2);
  }
  if (quality === "affordable") {
    if (boardId === "plpb") {
      if (numThk === 11) return 27;
      if (numThk === 17) return 29;
      if (numThk === 18) return 34;
      if (numThk === 25) return 42;
    }
    if (boardId === "hdhmr") {
      if (Math.abs(numThk - 16.75) < 0.1) return 88;
      if (numThk === 18) return 99;
      if (numThk === 25) return 135;
    }
    if (boardId === "ply_laminate") {
      if (numThk === 6) return 22;
      if (numThk === 9) return 35;
      if (numThk === 12) return 38;
      if (numThk === 15) return 46;
      if (numThk === 16) return 46;
      if (numThk === 18) return 55;
    }
    if (boardId === "mdf") {
      if (numThk === 17) return 55;
      if (numThk === 18) return 60;
      if (numThk === 25) return 80;
      if (numThk === 35) return 112;
    }
  } else {
    // Standard quality logic
    if (boardId === "plpb") {
      if (numThk === 18) return 49;
      if (numThk === 25) return 63;
      if (numThk === 36) return 98;
    }
    if (boardId === "hdhmr") {
      if (numThk === 25) return 108;
    }
    if (boardId === "mdf") {
      if (numThk === 18) return 61;
      if (numThk === 25) return 83;
      if (numThk === 36) return 122;
    }
    if (boardId === "bwr_plywood") {
      if (numThk === 18) return 74;
    }
    if (boardId === "bwp_plywood") {
      if (numThk === 18) return 110;
    }
  }
  
  // Default fallback scaling
  return baseRate * (numThk / 18);
};"""

import sys
if old_func not in content:
    # try looser match
    print("WARNING: Exact match failed")
    
content = content.replace(old_func, new_func)
with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
