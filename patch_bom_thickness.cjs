const fs = require('fs');
let content = fs.readFileSync('src/pages/ProjectDetails.tsx', 'utf-8');

let searchStr = "      let defaultThickness = '18mm';\n      let defaultMaterial = 'Board';\n      const nameMatch = item.name.match(/\\(([\\w_]+)\\)/);";
let replaceStr = "      let defaultThickness = '18mm';\n      let defaultMaterial = 'Board';\n      \n      if (item.config?.boardThickness) {\n          defaultThickness = item.config.boardThickness + 'mm';\n      }\n      if (item.config?.boardId) {\n          const bId = item.config.boardId.toLowerCase();\n          if (bId.includes('particle') || bId.includes('plpb')) defaultMaterial = 'Particle Board';\n          else if (bId.includes('mdf')) defaultMaterial = 'MDF';\n          else if (bId.includes('plywood') || bId.includes('ply')) defaultMaterial = 'Plywood';\n          else if (bId.includes('hdhmr')) defaultMaterial = 'HDHMR';\n      }\n\n      const nameMatch = item.name.match(/\\(([\\w_]+)\\)/);";

content = content.replace(searchStr, replaceStr);

fs.writeFileSync('src/pages/ProjectDetails.tsx', content);
console.log("Patched thickness extraction");
