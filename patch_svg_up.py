import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                  onPointerUp={(e) => {
                    if (dragState) {
                       setDragState(null);
                       setTimeout(() => { isDraggingRef.current = false; }, 50);
                    }
                  }}"""

replacement = """                  onPointerUp={(e) => {
                    if (isDrawingAngular && currentAngularShelf) {
                        const dist = Math.hypot(currentAngularShelf.x2 - currentAngularShelf.x1, currentAngularShelf.y2 - currentAngularShelf.y1);
                        if (dist > 10) {
                            setAngularShelves(prev => [...prev, { ...currentAngularShelf, id: Date.now().toString() }]);
                        }
                        setCurrentAngularShelf(null);
                        return;
                    }
                    if (dragState) {
                       setDragState(null);
                       setTimeout(() => { isDraggingRef.current = false; }, 50);
                    }
                  }}"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
