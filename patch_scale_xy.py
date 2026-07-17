import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace dx * scale with dx * scaleX and dy * scale with dy * scaleY for Wooden
wooden_target = """                    if (type === 'h') {
                        if (bayH === undefined) return;
                        let hPositions = bay.shelfOffsets || {};
                        let currentRel = hPositions[idx];
                        if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.shelves || 0) + 1);
                        }
                        
                        let deltaRel = (dy * scale) / bayH;"""
                        
wooden_replace = """                    if (type === 'h') {
                        if (bayH === undefined) return;
                        let hPositions = bay.shelfOffsets || {};
                        let currentRel = hPositions[idx];
                        if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.shelves || 0) + 1);
                        }
                        
                        let deltaRel = (dy * scaleY) / bayH;"""
content = content.replace(wooden_target, wooden_replace)

v_target = """                         let currentRel = vPositions[idx];
                         if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.verticalShelves || 0) + 1);
                         }
                         
                         let deltaRel = (dx * scale) / bayW;"""
v_replace = """                         let currentRel = vPositions[idx];
                         if (currentRel === undefined) {
                            currentRel = (idx + 1) / ((bay.verticalShelves || 0) + 1);
                         }
                         
                         let deltaRel = (dx * scaleX) / bayW;"""
content = content.replace(v_target, v_replace)

main_v_target = """                    } else if (type === 'main_v') {
                        let currentRel = colOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numBays;
                        }
                        let deltaRel = (dx * scale) / (width - 16); // Total drawW without padding is roughly width"""
main_v_replace = """                    } else if (type === 'main_v') {
                        let currentRel = colOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numBays;
                        }
                        let deltaRel = (dx * scaleX) / (width - 16); // Total drawW without padding is roughly width"""
content = content.replace(main_v_target, main_v_replace)

main_h_target = """                    } else if (type === 'main_h') {
                        let currentRel = rowOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numRows;
                        }
                        let deltaRel = (dy * scale) / (height - 16); // Total drawH without padding is roughly height"""
main_h_replace = """                    } else if (type === 'main_h') {
                        let currentRel = rowOffsets[idx];
                        if (currentRel === undefined) {
                           currentRel = (idx + 1) / numRows;
                        }
                        let deltaRel = (dy * scaleY) / (height - 16); // Total drawH without padding is roughly height"""
content = content.replace(main_h_target, main_h_replace)


with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
