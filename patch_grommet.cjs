const fs = require('fs');

function patchLshape() {
    let content = fs.readFileSync('src/pages/LShapeTableCalculator.tsx', 'utf8');
    
    // Default values
    content = content.replace(
        /useState<string>\("grommet"\); \/\/ 'grommet', 'raceway', 'none'/g,
        'useState<string>("raceway"); // \'raceway\', \'none\''
    );
    content = content.replace(
        /useState<string>\("grommet"\);/g,
        'useState<string>("raceway");'
    );
    
    // Remove options
    content = content.replace(/<option value="grommet">PVC Grommets<\/option>\n/g, '');
    
    fs.writeFileSync('src/pages/LShapeTableCalculator.tsx', content);
}

function patchWorkstation() {
    let content = fs.readFileSync('src/pages/WorkstationCalculator.tsx', 'utf8');
    
    // Remove options
    content = content.replace(/<option value="grommet">\s*PVC Grommets \(x2 for ₹\{GROMMET_COST \* 2\}\)\s*<\/option>\n/g, '');
    content = content.replace(/<option value="grommet">PVC Grommets<\/option>\n/g, '');
    
    fs.writeFileSync('src/pages/WorkstationCalculator.tsx', content);
}

patchLshape();
patchWorkstation();
console.log("Patched grommets");
