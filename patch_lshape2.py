import re

with open('src/pages/LShapeTableCalculator.tsx', 'r') as f:
    content = f.read()

replacement = """
  let topPerimeterM = (mainWidth * 2 + mainDepth * 2) / 1000;
  if (includeReturnStorage) {
    topPerimeterM += (returnWidth * 2 + returnDepth * 2) / 1000;
    topPerimeterM -= (2 * Math.min(mainDepth, returnDepth)) / 1000;
  }
  topPerimeterM *= 1.2; // 20% wastage

  // Edge Banding for Table Tops (only for Wood tops)
"""
content = re.sub(
    r'\n  // Edge Banding for Table Tops \(only for Wood tops\)',
    replacement,
    content
)

with open('src/pages/LShapeTableCalculator.tsx', 'w') as f:
    f.write(content)
