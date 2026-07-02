import * as fs from 'fs';

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// The issue was onClick=\{([^}]+)\}, which failed on onClick={() => ... toggleDoor(`bay-${idx}`)} because of the `}` inside `${idx}`.
// We can just match the onClick loosely or exactly since we know the structure.
// Let's use a replacer for all `<g className={isFullScreenDrawing ? ...` up to `</g>`

let newContent = content.replace(
  /<g\s+className=\{isFullScreenDrawing \? "cursor-pointer hover:opacity-80 transition-opacity" : ""\}\s+onClick=\{([^>]+)\}\s*>\s*\{!([^?]+)\s*\?\s*\(\s*<>\s*([\s\S]*?)\s*<\/>\s*\)\s*:\s*\(\s*<>\s*([\s\S]*?)\s*<\/>\s*\)\s*\}\s*<\/g>/g,
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
