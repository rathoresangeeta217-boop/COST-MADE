import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                    if (type === 'h') {"""

replacement = """                    if (type === 'angular_endpoint' && dragState.shelfId) {
                        const shelfId = dragState.shelfId;
                        setAngularShelves(prev => prev.map(s => {
                            if (s.id === shelfId) {
                                if (idx === 1) {
                                    return { ...s, x1: s.x1 + dx * scaleX, y1: s.y1 + dy * scaleY };
                                } else {
                                    return { ...s, x2: s.x2 + dx * scaleX, y2: s.y2 + dy * scaleY };
                                }
                            }
                            return s;
                        }));
                        setDragState({...dragState, startX: e.clientX, startY: e.clientY});
                        return;
                    }
                    if (type === 'h') {"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
