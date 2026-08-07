import re

with open('src/pages/ProjectDetails.tsx', 'r') as f:
    content = f.read()

pattern = """             // If we found valid width/length, we can add it to pieces array
             if (pw && pl) {
               boardAggregation[key].pieces.push({ w: pw, l: pl, qty: pqty });
             } else if (area > 0) {
               // Fallback: If we just have area, approximate it as a square piece
               const side = Math.sqrt(area * 90000);
               boardAggregation[key].pieces.push({ w: side, l: side, qty: pqty });
             }"""

replacement = """             // If we found valid width/length, we can add it to pieces array
             if (pw && pl) {
               boardAggregation[key].pieces.push({ w: pw, l: pl, qty: pqty });
             } else if (area > 0) {
               // Fallback: If we just have area, approximate it as a square piece
               let sideW = Math.sqrt(area * 90000);
               let sideL = Math.sqrt(area * 90000);
               
               // Use b.l and b.w directly if they exist on the object (as they do in Custom Storage)
               if (b.l && b.w) {
                   sideW = b.w;
                   sideL = b.l;
               }

               boardAggregation[key].pieces.push({ w: sideW, l: sideL, qty: pqty });
             }"""

content = content.replace(pattern, replacement)

with open('src/pages/ProjectDetails.tsx', 'w') as f:
    f.write(content)
