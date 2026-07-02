const fs = require('fs');
let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// The line is: </text></>} />
// But we only want to replace it for shutter_solid, shutter_glass, shutters_double, 1_drawer (actually 1_drawer has NO shelves!).
// So let's do it manually via split and join or more precise string replace.

let lines = content.split('\n');

for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('</text></>} />')) {
    let textLine = lines[i - 1];
    
    if (textLine.includes('{Math.round(bayW)}x{Math.round(bayH)}')) {
       // This is shutter_solid, shutter_glass, shutters_double, 1_drawer
       // Wait, we don't want shelves for 1_drawer!
       // Let's check the style.
       let styleFound = "";
       for (let j = i; j >= 0; j--) {
          if (lines[j].includes('bay.style ===')) {
             styleFound = lines[j];
             break;
          }
       }
       
       if (styleFound.includes('shutter_solid') || styleFound.includes('shutter_glass') || styleFound.includes('shutters_double')) {
          lines[i] = lines[i].replace('</text></>} />', '</text>{renderShelves(bay, idx, bayX, bayY, bayW, bayH)}</>} />');
       }
    }
    
    if (textLine.includes('{Math.round(bayW)}x{Math.round(shutterH)}')) {
       lines[i] = lines[i].replace('</text></>} />', '</text>{renderShelves(bay, idx, bayX, shutterY, bayW, shutterH)}</>} />');
    }
  }
}

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', lines.join('\n'));
console.log("Patched childrenOpen manually");
