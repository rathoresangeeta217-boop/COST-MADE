const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// Update toggleDoor to also handle partitions
content = content.replace(
  /const toggleDoor = \(id: string\) => \{/,
  `const togglePartition = (partitionId: string, bayIdx: number) => {
    const newBays = [...bays];
    const bay = newBays[bayIdx];
    const removed = new Set(bay.removedPartitions || []);
    if (removed.has(partitionId)) {
      removed.delete(partitionId);
    } else {
      removed.add(partitionId);
    }
    bay.removedPartitions = Array.from(removed);
    setBays(newBays);
  };

  const toggleDoor = (id: string) => {`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated toggleDoor!");
