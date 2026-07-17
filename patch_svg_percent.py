import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Metal SVG
target = r'width=\{\(width \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4}'
content = re.sub(target, replace, content)

target = r'height=\{\(height \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4}'
content = re.sub(target, replace, content)


# Drawer SVG
target = r'width=\{\(drawerWidth \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (drawerWidth + 100) * 0.4}'
content = re.sub(target, replace, content)

target = r'height=\{\(drawerHeight \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (drawerHeight + 100) * 0.4}'
content = re.sub(target, replace, content)


# Locker SVG
target = r'width=\{\(computedLockerWidth \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerWidth + 100) * 0.4}'
content = re.sub(target, replace, content)

target = r'height=\{\(computedLockerHeight \+ 100\) \* \(isFullScreenDrawing \? 1\.5 \* zoomLevel : 0\.4\)\}'
replace = r'height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (computedLockerHeight + 100) * 0.4}'
content = re.sub(target, replace, content)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

