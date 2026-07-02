const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// Replace {p.qty} with {Number.isInteger(p.qty) ? p.qty : Number(p.qty).toFixed(2)}
content = content.replace(/<td className="p-3 text-center font-bold">\{p\.qty\}<\/td>/g, 
  '<td className="p-3 text-center font-bold">{Number.isInteger(p.qty) ? p.qty : Number(p.qty).toFixed(2)}</td>');

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated p.qty rendering!");
