import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

pattern = r'<svg\s+viewBox={`0 0 \$\{width \+ 100\} \$\{height \+ 100\}`}\s+width=\{\(width \+ 100\) \* 0\.4 \* \(isFullScreenDrawing \? zoomLevel : 1\)\}\s+height=\{\(height \+ 100\) \* 0\.4 \* \(isFullScreenDrawing \? zoomLevel : 1\)\}\s+className="drop-shadow-2xl transition-all duration-200"\s+xmlns="http://www.w3.org/2000/svg"'

replace = r'''<svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={(width + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  height={(height + 100) * (isFullScreenDrawing ? 1.5 * zoomLevel : 0.4)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"'''

content = re.sub(pattern, replace, content)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

