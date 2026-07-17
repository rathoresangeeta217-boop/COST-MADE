import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# For Metal
metal_target = """                     const scale = 1 / (0.4 * (isFullScreenDrawing ? zoomLevel : 1));
                     if (type === 'main_h') {"""

metal_replace = """                     const svgEl = e.currentTarget as SVGSVGElement;
                     const rect = svgEl.getBoundingClientRect();
                     const viewBoxHeight = height + 100;
                     const scale = viewBoxHeight / rect.height;
                     
                     if (type === 'main_h') {"""
content = content.replace(metal_target, metal_replace)

# For Wooden
wooden_target = """                    const scale = 1 / (0.4 * (isFullScreenDrawing ? zoomLevel : 1));
                    
                    if (type === 'h') {"""

wooden_replace = """                    const svgEl = e.currentTarget as SVGSVGElement;
                    const rect = svgEl.getBoundingClientRect();
                    const viewBoxHeight = height + 100;
                    const viewBoxWidth = width + 100;
                    const scaleY = viewBoxHeight / rect.height;
                    const scaleX = viewBoxWidth / rect.width;
                    const scale = scaleY; // Use Y scale for general mapping
                    
                    if (type === 'h') {"""
content = content.replace(wooden_target, wooden_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

