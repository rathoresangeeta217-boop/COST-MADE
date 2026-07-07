import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Replace sideH with baySideH inside the three bays.forEach loops.
# First loop starts at line 538: bays.forEach((bay, index) => {
# Second loop starts at line 655: bays.forEach((bay, index) => {
# Third loop starts at line 774: bays.forEach((bay, index) => {

# First, let's fix the first loop where we missed some `sideH`
content = content.replace('l: sideH - 20,', 'l: baySideH - 20,')
content = content.replace('l: sideH,', 'l: baySideH,')
# But wait, there is a `l: isHoriz ? (width - thickness * 2) : sideH,` which will become `l: isHoriz ? (width - thickness * 2) : baySideH,` which is wrong (should be sideH for vertical partitions).
# So I should change that specific one back:
content = content.replace('l: isHoriz ? (width - thickness * 2) : baySideH,', 'l: isHoriz ? (width - thickness * 2) : sideH,')
content = content.replace('ebMm: (isHoriz ? (width - thickness * 2) : baySideH) * numPartitions,', 'ebMm: (isHoriz ? (width - thickness * 2) : sideH) * numPartitions,')
content = content.replace('sideH * numPartitions', 'sideH * numPartitions') # no change

# Now the other usages of sideH inside the loops:
# We can just replace `sideH` with `baySideH` in specific known lines.
# Line 656: const shH = Math.max(0, sideH - 4);
content = content.replace('const shH = Math.max(0, sideH - 4);', 'const shH = Math.max(0, baySideH - 4);')
# Line 663: const boxH = Math.max(0, (sideH - 4) / rows);
content = content.replace('const boxH = Math.max(0, (sideH - 4) / rows);', 'const boxH = Math.max(0, (baySideH - 4) / rows);')
# Line 684: const faceH = Math.min(154, Math.max(0, Math.round(sideH / 3)));
content = content.replace('const faceH = Math.min(154, Math.max(0, Math.round(sideH / 3)));', 'const faceH = Math.min(154, Math.max(0, Math.round(baySideH / 3)));')
# Line 685: const shutterH = Math.max(0, sideH - faceH - 4);
content = content.replace('const shutterH = Math.max(0, sideH - faceH - 4);', 'const shutterH = Math.max(0, baySideH - faceH - 4);')
# Line 725: const faceH = Math.max(0, Math.round(sideH / 3) - 4);
content = content.replace('const faceH = Math.max(0, Math.round(sideH / 3) - 4);', 'const faceH = Math.max(0, Math.round(baySideH / 3) - 4);')
# Line 736: const faceH = Math.max(0, Math.round(sideH / 2) - 4);
content = content.replace('const faceH = Math.max(0, Math.round(sideH / 2) - 4);', 'const faceH = Math.max(0, Math.round(baySideH / 2) - 4);')
# Line 747: const faceH = Math.max(0, sideH - 4);
content = content.replace('const faceH = Math.max(0, sideH - 4);', 'const faceH = Math.max(0, baySideH - 4);')

# Loop 3
# Line 779: dh = Math.max(80, Math.round(sideH / 3) - 60);
content = content.replace('dh = Math.max(80, Math.round(sideH / 3) - 60);', 'dh = Math.max(80, Math.round(baySideH / 3) - 60);')
# Line 782: dh = Math.max(100, Math.round(sideH / 2) - 60);
content = content.replace('dh = Math.max(100, Math.round(sideH / 2) - 60);', 'dh = Math.max(100, Math.round(baySideH / 2) - 60);')
# Line 785: dh = Math.max(100, sideH - 60);
content = content.replace('dh = Math.max(100, sideH - 60);', 'dh = Math.max(100, baySideH - 60);')

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
