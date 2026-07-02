const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// For shutter_solid (main bay door):
// The text inside childrenOpen looks like:
// <text x={bayX + bayW / 2} y={bayY + bayH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
//   {Math.round(bayW)}x{Math.round(bayH)}
// </text></>} />
content = content.replace(
  /(\<text x=\{bayX \+ bayW \/ 2\} y=\{bayY \+ bayH \/ 2\} textAnchor="middle" dominantBaseline="middle" fill="\#94a3b8" fontSize="12px" fontFamily="monospace"\>\s*\{Math\.round\(bayW\)\}x\{Math\.round\(bayH\)\}\s*\<\/text\>)(\<\/\} \/\>)/g,
  '$1{renderShelves(bay, idx, bayX, bayY, bayW, bayH)}$2'
);

// For 1_drawer_1_shutter (main shutter below drawer):
// <text x={bayX + bayW / 2} y={shutterY + shutterH / 2} textAnchor="middle" dominantBaseline="middle" fill="#94a3b8" fontSize="12px" fontFamily="monospace">
//   {Math.round(bayW)}x{Math.round(shutterH)}
// </text></>} />
content = content.replace(
  /(\<text x=\{bayX \+ bayW \/ 2\} y=\{shutterY \+ shutterH \/ 2\} textAnchor="middle" dominantBaseline="middle" fill="\#94a3b8" fontSize="12px" fontFamily="monospace"\>\s*\{Math\.round\(bayW\)\}x\{Math\.round\(shutterH\)\}\s*\<\/text\>)(\<\/\} \/\>)/g,
  '$1{renderShelves(bay, idx, bayX, shutterY, bayW, shutterH)}$2'
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Patched childrenOpen for solid and double shutters");
