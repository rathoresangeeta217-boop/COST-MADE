const fs = require('fs');
['src/pages/WorkstationCalculator.tsx', 'src/pages/LShapeTableCalculator.tsx'].forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(
    /<option value="straight">Straight Leg<\/option>\s*<option value="u_shape">U-Shape Leg<\/option>/,
    `<option value="straight">Straight Leg</option>
                        <option value="u_shape">U-Shape Leg</option>
                        <option value="angular">Angular Leg</option>`
  );
  fs.writeFileSync(file, content);
});
console.log("Patched");
