import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

getBoardsNew = """export const getBoards = (quality: string, category: string = "wooden") => {
  if (category === "metal") {
    return [
      { id: "crca_powder_coated", name: "Powder Coated CRCA Metal", costPerSqFt: quality === "affordable" ? 150 : 220 },
      { id: "ss_304", name: "Stainless Steel 304", costPerSqFt: quality === "affordable" ? 350 : 450 },
    ];
  }
  return [
    { id: "plpb", name: "PLPB", costPerSqFt: quality === "affordable" ? 34 : 49 },
    { id: "mdf", name: "MDF", costPerSqFt: quality === "affordable" ? 38 : 61 },
    {
      id: "hdhmr",
      name: "HDHMR",
      costPerSqFt: quality === "affordable" ? 99 : 74,
    },
    {
      id: "ply_laminate",
      name: "PLY LAMINATE",
      costPerSqFt: quality === "affordable" ? 55 : 130,
    },
    { id: "hdhmr_laminate", name: "HDHMR LAMINATE", costPerSqFt: 130 },
    {
      id: "ply_century_one_mm_laminate",
      name: "PLY CENTURY ONE MM LAMINATE",
      costPerSqFt: 230,
    },
  ];
};"""

content = re.sub(
    r'export const getBoards = \(quality: string\) => \[\n.*?\n\];',
    getBoardsNew,
    content,
    flags=re.DOTALL
)

getThicknessNew = """export const getAvailableThicknesses = (
  boardId: string,
  quality: string,
): number[] => {
  if (boardId === "crca_powder_coated" || boardId === "ss_304") {
    return [0.8, 1, 1.2, 1.6, 2];
  }
"""

content = re.sub(
    r'export const getAvailableThicknesses = \(\n  boardId: string,\n  quality: string,\n\): number\[\] => \{\n',
    getThicknessNew,
    content
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
