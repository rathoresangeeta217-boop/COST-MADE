import * as fs from 'fs';

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

let newContent = content.replace(
  /<g\s+className=\{isFullScreenDrawing \? "cursor-pointer hover:opacity-80 transition-opacity" : ""\}\s+onClick=\{([\s\S]*?)\}\s*>\s*\{!([^?]+)\s*\?\s*\(\s*<>\s*([\s\S]*?)\s*<\/>\s*\)\s*:\s*\(\s*<>\s*([\s\S]*?)\s*<\/>\s*\)\s*\}\s*<\/g>/g,
  (match, p1, p2, p3, p4) => {
    return `<AnimatedDoorGroup className={isFullScreenDrawing ? "cursor-pointer hover:opacity-80 transition-opacity" : ""} onClick={${p1}} isOpen={${p2.trim()}} childrenClosed={<>${p3}</>} childrenOpen={<>${p4}</>} />`;
  }
);

if (content !== newContent) {
  fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', newContent);
  console.log("Replaced!");
} else {
  console.log("No replacements made.");
}
