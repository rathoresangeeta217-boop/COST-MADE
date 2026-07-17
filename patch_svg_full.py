import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Metal storage SVG
metal_svg_target = """<svg width="100%" height="auto" viewBox={`-50 -50 ${width + 100} ${height + 100}`} className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "w-full max-h-[90vh]" : "max-h-[600px] w-auto"}`}>"""
metal_svg_replace = """<svg width="100%" height="auto" viewBox={`-50 -50 ${width + 100} ${height + 100}`} className={`drop-shadow-md transition-all duration-200 ${isFullScreenDrawing ? "w-full h-full" : "max-h-[600px] w-auto"}`} style={{ transform: isFullScreenDrawing ? `scale(${zoomLevel})` : 'none' }}>"""
content = content.replace(metal_svg_target, metal_svg_replace, 1)

# Wood storage SVG
wood_svg_target = """                <svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={(width + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  height={(height + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  className="drop-shadow-2xl transition-all duration-200"
                  xmlns="http://www.w3.org/2000/svg"
                >"""
wood_svg_replace = """                <svg
                  viewBox={`0 0 ${width + 100} ${height + 100}`}
                  width={isFullScreenDrawing ? "100%" : (width + 100) * 0.4}
                  height={isFullScreenDrawing ? "100%" : (height + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "w-full h-full" : "max-h-[600px] w-auto"}`}
                  style={{ transform: isFullScreenDrawing ? `scale(${zoomLevel})` : 'none' }}
                  xmlns="http://www.w3.org/2000/svg"
                >"""
content = content.replace(wood_svg_target, wood_svg_replace, 1)

# Drawer SVG
drawer_svg_target = """                <svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={(drawerWidth + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  height={(drawerHeight + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  className="drop-shadow-2xl transition-all duration-200"
                  xmlns="http://www.w3.org/2000/svg"
                >"""
drawer_svg_replace = """                <svg
                  viewBox={`-50 -50 ${drawerWidth + 100} ${drawerHeight + 100}`}
                  width={isFullScreenDrawing ? "100%" : (drawerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? "100%" : (drawerHeight + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "w-full h-full" : "max-h-[600px] w-auto"}`}
                  style={{ transform: isFullScreenDrawing ? `scale(${zoomLevel})` : 'none' }}
                  xmlns="http://www.w3.org/2000/svg"
                >"""
content = content.replace(drawer_svg_target, drawer_svg_replace, 1)

# Locker SVG
locker_svg_target = """                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={(computedLockerWidth + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  height={(computedLockerHeight + 100) * 0.4 * (isFullScreenDrawing ? zoomLevel : 1)}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "w-full max-h-[90vh]" : "max-h-[600px] w-auto"}`}
                  xmlns="http://www.w3.org/2000/svg"
                >"""
locker_svg_replace = """                <svg
                  viewBox={`-50 -50 ${computedLockerWidth + 100} ${computedLockerHeight + 100}`}
                  width={isFullScreenDrawing ? "100%" : (computedLockerWidth + 100) * 0.4}
                  height={isFullScreenDrawing ? "100%" : (computedLockerHeight + 100) * 0.4}
                  className={`drop-shadow-2xl transition-all duration-200 ${isFullScreenDrawing ? "w-full h-full" : "max-h-[600px] w-auto"}`}
                  style={{ transform: isFullScreenDrawing ? `scale(${zoomLevel})` : 'none' }}
                  xmlns="http://www.w3.org/2000/svg"
                >"""
content = content.replace(locker_svg_target, locker_svg_replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

