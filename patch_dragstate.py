import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """  const [dragState, setDragState] = useState<{
    bayIdx: number;
    type: 'h' | 'v';
    idx: number;
    startX: number;
    startY: number;
    bayX: number;
    bayY: number;
    bayW: number;
    bayH: number;
    isDragging: boolean;
    partitionId: string;
  } | null>(null);"""

replacement = """  const [dragState, setDragState] = useState<{
    bayIdx: number;
    type: 'h' | 'v' | 'main_h' | 'main_v' | 'angular_endpoint';
    idx: number;
    startX: number;
    startY: number;
    bayX: number;
    bayY: number;
    bayW: number;
    bayH: number;
    isDragging: boolean;
    partitionId: string;
    shelfId?: string;
  } | null>(null);"""

content = content.replace(target, replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
