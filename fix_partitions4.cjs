const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const oldTotalShelves = `      // Internal Shelves for this bay
      if (bay.shelves > 0) {
        totalShelvesCount += bay.shelves;
      }
      if (bay.verticalShelves && bay.verticalShelves > 0) {
        totalVerticalShelvesCount += bay.verticalShelves;
      }`;

const newTotalShelves = `      // Internal Shelves for this bay (segmented calculation)
      const cols = (bay.verticalShelves || 0) + 1;
      const rows = (bay.shelves || 0) + 1;
      let removedH = 0;
      let removedV = 0;
      (bay.removedPartitions || []).forEach(p => {
        if (p.startsWith('h-')) removedH++;
        if (p.startsWith('v-')) removedV++;
      });
      
      if (bay.shelves > 0) {
        totalShelvesCount += bay.shelves - (removedH / cols);
      }
      if (bay.verticalShelves && bay.verticalShelves > 0) {
        totalVerticalShelvesCount += bay.verticalShelves - (removedV / rows);
      }`;

if (content.includes(oldTotalShelves)) {
  content = content.replace(oldTotalShelves, newTotalShelves);
  fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
  console.log("Updated totalShelvesCount calculation!");
} else {
  console.log("Could not find old totalShelvesCount calculation");
}
