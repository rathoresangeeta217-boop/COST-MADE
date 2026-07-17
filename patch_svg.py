import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                <svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                  onPointerMove={(e) => {"""

replacement = """                <svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={isFullScreenDrawing ? `${100 * zoomLevel}%` : (width + 100) * 0.4}
                  height={isFullScreenDrawing ? `${100 * zoomLevel}%` : (height + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "m-auto" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                  onPointerDown={(e) => {
                     if (isDrawingAngular) {
                        e.preventDefault();
                        const svgEl = e.currentTarget as SVGSVGElement;
                        const rect = svgEl.getBoundingClientRect();
                        const viewBoxHeight = height + 100;
                        const viewBoxWidth = width + 100;
                        const scaleX = viewBoxWidth / rect.width;
                        const scaleY = viewBoxHeight / rect.height;
                        const x = (e.clientX - rect.left) * scaleX;
                        const y = (e.clientY - rect.top) * scaleY;
                        setCurrentAngularShelf({ x1: x, y1: y, x2: x, y2: y });
                     }
                  }}
                  onPointerMove={(e) => {
                    if (isDrawingAngular && currentAngularShelf) {
                        const svgEl = e.currentTarget as SVGSVGElement;
                        const rect = svgEl.getBoundingClientRect();
                        const viewBoxHeight = height + 100;
                        const viewBoxWidth = width + 100;
                        const scaleX = viewBoxWidth / rect.width;
                        const scaleY = viewBoxHeight / rect.height;
                        const x = (e.clientX - rect.left) * scaleX;
                        const y = (e.clientY - rect.top) * scaleY;
                        setCurrentAngularShelf({ ...currentAngularShelf, x2: x, y2: y });
                        return;
                    }

"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
