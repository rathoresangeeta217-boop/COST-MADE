import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# For Drawer
drawer_pattern = r'<svg\s+viewBox={`-50 -50 \$\{drawerWidth \+ 100\} \$\{drawerHeight \+ 100\}`}\s+width=\{isFullScreenDrawing \? "100%" : \(drawerWidth \+ 100\) \* 0\.4\}\s+height=\{isFullScreenDrawing \? "100%" : \(drawerHeight \+ 100\) \* 0\.4\}\s+className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`}\s+style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}\s+xmlns="http://www.w3.org/2000/svg"\s+>'
drawer_replace = r'''<svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={(drawerWidth + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(drawerHeight + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >'''
content = re.sub(drawer_pattern, drawer_replace, content)

# For Locker
locker_pattern = r'<svg\s+viewBox={`-50 -50 \$\{computedLockerWidth \+ 100\} \$\{computedLockerHeight \+ 100\}`}\s+width=\{isFullScreenDrawing \? "100%" : \(computedLockerWidth \+ 100\) \* 0\.4\}\s+height=\{isFullScreenDrawing \? "100%" : \(computedLockerHeight \+ 100\) \* 0\.4\}\s+className={`drop-shadow-2xl transition-all duration-200 \$\{isFullScreenDrawing \? "w-full h-full" : "max-h-\[600px\] w-auto"\}`}\s+style=\{\{ transform: isFullScreenDrawing \? `scale\(\$\{zoomLevel\}\)` : \'none\' \}\}\s+xmlns="http://www.w3.org/2000/svg"\s+>'
locker_replace = r'''<svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={(computedLockerWidth + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(computedLockerHeight + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >'''
content = re.sub(locker_pattern, locker_replace, content)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

