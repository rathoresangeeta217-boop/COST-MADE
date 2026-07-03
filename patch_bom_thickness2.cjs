const fs = require('fs');
let content = fs.readFileSync('src/pages/ProjectDetails.tsx', 'utf-8');

let replaceStr = `
      if (nameMatch && !item.config?.boardThickness) {
        const boardId = nameMatch[1];
`;

content = content.replace(/if \(nameMatch\) \{/g, replaceStr);

fs.writeFileSync('src/pages/ProjectDetails.tsx', content);
console.log("Patched thickness extraction to be safer");
