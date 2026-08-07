import re

with open('src/pages/ProjectDetails.tsx', 'r') as f:
    content = f.read()

pattern = """             // If we found valid width/length, we can add it to pieces array
             if (pw && pl) {
               boardAggregation[key].pieces!.push({ w: pw, l: pl, qty: pqty });
             } else if (area > 0) {
               // Fallback: If we just have area, approximate it as a square piece, unless it is a back panel where we want the actual size 
               let sideW = Math.sqrt(area * 90000);
               let sideL = Math.sqrt(area * 90000);
               if (label.includes("Back Panel")) {
                  // For a back panel, it's typically the overall W x H. We can try to extract from config if possible, or leave as square.
                  // Try to find the back panel size from label.
                  // For now, let's keep it as square if not explicitly defined.
               }
               boardAggregation[key].pieces!.push({ w: sideW, l: sideL, qty: pqty });
             }"""

replacement = """             // If we found valid width/length, we can add it to pieces array
             if (pw && pl) {
               boardAggregation[key].pieces!.push({ w: pw, l: pl, qty: pqty });
             } else if (area > 0) {
               // Fallback: If we just have area, approximate it as a square piece, unless it is a back panel where we want the actual size 
               let sideW = Math.sqrt(area * 90000);
               let sideL = Math.sqrt(area * 90000);
               
               // Try extracting W/H from b.l and b.w since for custom storage they might be set on the piece object directly
               if (b.l && b.w) {
                   sideW = b.w;
                   sideL = b.l;
               }

               boardAggregation[key].pieces!.push({ w: sideW, l: sideL, qty: pqty });
             }"""

content = content.replace(pattern, replacement)

with open('src/pages/ProjectDetails.tsx', 'w') as f:
    f.write(content)
