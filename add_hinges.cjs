const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
const lines = content.split('\n');

// Line numbers might change, so we will look for patterns.
// We want to inject hinges for the shutters.

function inject(lineRange, injectString) {
    for (let i = lineRange[0]; i <= lineRange[1]; i++) {
        if (lines[i].includes('fill="rgba(0,0,0,0.2)"')) {
            // Find where the rect ends
            for (let j = i; j < i + 10; j++) {
                if (lines[j].includes('/>')) {
                    lines.splice(j + 1, 0, injectString);
                    break;
                }
            }
            break;
        }
    }
}

// 1. Box Shutter
inject([2078, 2090], `                                            {/* Hinges */}\n                                            <rect x={boxX + 2} y={boxY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                            <rect x={boxX + 2} y={boxY + boxH - 35} width="4" height="15" fill="#94a3b8" rx="1" />`);

// 2. Solid Shutter
inject([2133, 2145], `                                    {/* Hinges */}\n                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />`);

// 3. Glass Shutter
inject([2218, 2230], `                                    {/* Hinges */}\n                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />`);

// 4. Double Shutter
inject([2271, 2283], `                                    {/* Hinges */}\n                                    <rect x={bayX + 2} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                    <rect x={bayX + 2} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />\n                                    <rect x={bayX + bayW - 6} y={bayY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                    <rect x={bayX + bayW - 6} y={bayY + bayH - 35} width="4" height="15" fill="#94a3b8" rx="1" />`);

// 5. 1 Drawer 1 Shutter (shutter part)
inject([2511, 2525], `                                              {/* Hinges */}\n                                              <rect x={bayX + 2} y={shutterY + 20} width="4" height="15" fill="#94a3b8" rx="1" />\n                                              <rect x={bayX + 2} y={shutterY + shutterH - 35} width="4" height="15" fill="#94a3b8" rx="1" />`);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', lines.join('\n'));
console.log("Hinges injected successfully.");
