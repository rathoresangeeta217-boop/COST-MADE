const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf8');

// Inside calcData and drawerCalcData, define the helper
const helperFunc = `    const getCustomMat = (type, fallbackRate, fallbackName = "") => {
      let customId = "default";
      let thickness = 9;
      if (type === "shutter") { customId = shutterBoardId; thickness = boardThickness; }
      else if (type === "back") { customId = backPanelBoardId; thickness = 9; }
      else if (type === "drawer") { customId = drawerBoxBoardId; thickness = 9; }
      
      if (customId === "default") return { cost: fallbackRate, append: fallbackName };
      const b = boards.find(x => x.id === customId);
      if (!b) return { cost: fallbackRate, append: fallbackName };
      return { cost: getBoardRate(customId, b.costPerSqFt, thickness, quality) + totalMicaRate, append: \` (\${b.name} \${thickness}mm)\` };
    };
`;

content = content.replace(
  /const calcData = useMemo\(\(\) => \{\n\s*const thickness = boardThickness;/,
  `const calcData = useMemo(() => {
    const thickness = boardThickness;
${helperFunc}`
);

content = content.replace(
  /const drawerCalcData = useMemo\(\(\) => \{\n\s*const pieces: \{/,
  `const drawerCalcData = useMemo(() => {
${helperFunc}
    const pieces: {`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched calc helpers");
