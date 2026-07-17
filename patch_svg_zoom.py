import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Restore Metal Storage
target_metal = r'<svg width="100%" height="auto" viewBox={`-50 -50 \$\{width \+ 100\} \$\{height \+ 100\}`} className={`drop-shadow-md transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`} style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}>'
replace_metal = r'<svg width={(width + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)} height={(height + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)} viewBox={`-50 -50 ${width + 100} ${height + 100}`} className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}>'
content = re.sub(target_metal, replace_metal, content)

# Restore Wood Storage
target_wood = r'<svg\n                  viewBox={`0 0 \$\{width \+ 100\} \$\{height \+ 100\}`}\n                  width=\{isFullScreenDrawing \? "100%" : \(width \+ 100\) \* 0\.4\}\n                  height=\{isFullScreenDrawing \? "100%" : \(height \+ 100\) \* 0\.4\}\n                  className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`}\n                  style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}\n                  xmlns="http://www.w3.org/2000/svg"\n                >'
replace_wood = r'''<svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={(width + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(height + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >'''
content = content.replace(target_wood, replace_wood)

# Restore Drawer
target_drawer = r'<svg\n                  viewBox={`-50 -50 \$\{drawerWidth \+ 100\} \$\{drawerHeight \+ 100\}`}\n                  width=\{isFullScreenDrawing \? "100%" : \(drawerWidth \+ 100\) \* 0\.4\}\n                  height=\{isFullScreenDrawing \? "100%" : \(drawerHeight \+ 100\) \* 0\.4\}\n                  className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`}\n                  style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}\n                  xmlns="http://www.w3.org/2000/svg"\n                >'
replace_drawer = r'''<svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={(drawerWidth + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(drawerHeight + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >'''
content = content.replace(target_drawer, replace_drawer)

# Restore Locker
target_locker = r'<svg\n                  viewBox={`-50 -50 \$\{computedLockerWidth \+ 100\} \$\{computedLockerHeight \+ 100\}`}\n                  width=\{isFullScreenDrawing \? "100%" : \(computedLockerWidth \+ 100\) \* 0\.4\}\n                  height=\{isFullScreenDrawing \? "100%" : \(computedLockerHeight \+ 100\) \* 0\.4\}\n                  className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`}\n                  style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}\n                  xmlns="http://www.w3.org/2000/svg"\n                >'
replace_locker = r'''<svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={(computedLockerWidth + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(computedLockerHeight + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >'''
content = content.replace(target_locker, replace_locker)


with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

