import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """  const [isFullScreenDrawing, setIsFullScreenDrawing] = useState<boolean>(false);
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const isDraggingRef = useRef(false);
  const [openDoors, setOpenDoors] = useState<Set<string>>(new Set());"""

replacement = """  const [isFullScreenDrawing, setIsFullScreenDrawing] = useState<boolean>(false);
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const isDraggingRef = useRef(false);
  const [openDoors, setOpenDoors] = useState<Set<string>>(new Set());
  const [isDrawingAngular, setIsDrawingAngular] = useState(false);
  const [currentAngularShelf, setCurrentAngularShelf] = useState<{x1: number, y1: number, x2: number, y2: number} | null>(null);
  const [angularShelves, setAngularShelves] = useState<{id: string, x1: number, y1: number, x2: number, y2: number}[]>([]);"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
