import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# For type === 'h'
target_h = """                        let deltaRel = (dy * scale) / bayH;
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));"""
replace_h = """                        let deltaRel = (dy * scale) / bayH;
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (hPositions[idx - 1] ?? (idx / ((bay.shelves || 0) + 1))) : 0;
                        let nextRel = idx < (bay.shelves || 0) - 1 ? (hPositions[idx + 1] ?? ((idx + 2) / ((bay.shelves || 0) + 1))) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));"""
content = content.replace(target_h, replace_h, 1)

# For type === 'v'
target_v = """                         let deltaRel = (dx * scale) / bayW;
                         let newRel = currentRel + deltaRel;
                         newRel = Math.max(0.05, Math.min(0.95, newRel));"""
replace_v = """                         let deltaRel = (dx * scale) / bayW;
                         let newRel = currentRel + deltaRel;
                         let prevRel = idx > 0 ? (vPositions[idx - 1] ?? (idx / ((bay.verticalShelves || 0) + 1))) : 0;
                         let nextRel = idx < (bay.verticalShelves || 0) - 1 ? (vPositions[idx + 1] ?? ((idx + 2) / ((bay.verticalShelves || 0) + 1))) : 1;
                         newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));"""
content = content.replace(target_v, replace_v, 1)

# For type === 'main_v'
target_mv = """                        let deltaRel = (dx * scale) / (width - 16); // Total drawW without padding is roughly width
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));"""
replace_mv = """                        let deltaRel = (dx * scale) / (width - 16); // Total drawW without padding is roughly width
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (colOffsets[idx - 1] ?? (idx / numBays)) : 0;
                        let nextRel = idx < numBays - 1 ? (colOffsets[idx + 1] ?? ((idx + 2) / numBays)) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));"""
content = content.replace(target_mv, replace_mv, 1)

# For type === 'main_h'
target_mh = """                        let deltaRel = (dy * scale) / (height - 16); // Total drawH without padding is roughly height
                        let newRel = currentRel + deltaRel;
                        newRel = Math.max(0.05, Math.min(0.95, newRel));"""
replace_mh = """                        let deltaRel = (dy * scale) / (height - 16); // Total drawH without padding is roughly height
                        let newRel = currentRel + deltaRel;
                        let prevRel = idx > 0 ? (rowOffsets[idx - 1] ?? (idx / numRows)) : 0;
                        let nextRel = idx < numRows - 1 ? (rowOffsets[idx + 1] ?? ((idx + 2) / numRows)) : 1;
                        newRel = Math.max(prevRel + 0.05, Math.min(nextRel - 0.05, newRel));"""
content = content.replace(target_mh, replace_mh, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

