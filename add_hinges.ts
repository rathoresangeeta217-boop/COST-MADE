import * as fs from 'fs';

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

function injectHinges(content: string, searchStr: string, hingesCode: string): string {
    const idx = content.indexOf(searchStr);
    if (idx === -1) {
        console.error("Could not find string:\n" + searchStr);
        return content;
    }
    return content.slice(0, idx + searchStr.length) + "\n" + hingesCode + content.slice(idx + searchStr.length);
}

// 1. Box Shutter
content = injectHinges(
    content,
    `isOpen={isOpen} childrenClosed={<><rect\n                                        x={boxX + 2}\n                                        y={boxY + 2}\n                                        width={boxW - 4}\n                                        height={boxH - 4}\n                                        fill="#475569"\n                                        stroke="#334155"\n                                        strokeWidth="1"\n                                        rx="2"\n                                      />`,
    `                                      <rect x={boxX + 2} y={boxY + 10} width="3" height="12" fill="#94a3b8" rx="1" />\n                                      <rect x={boxX + 2} y={boxY + boxH - 22} width="3" height="12" fill="#94a3b8" rx="1" />`
);
// Wait, the search string was for childrenClosed. I should inject it into childrenOpen!
