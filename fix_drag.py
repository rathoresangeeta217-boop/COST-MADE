import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Edit 1: Add useRef to import
content = content.replace('import { useState, useMemo, useEffect } from "react";', 'import { useState, useMemo, useEffect, useRef } from "react";')

# Edit 2: Add isDraggingRef
content = content.replace('const [zoomLevel, setZoomLevel] = useState<number>(1);', 'const [zoomLevel, setZoomLevel] = useState<number>(1);\n  const isDraggingRef = useRef(false);')

# Edit 3: Update SVG onPointerMove to sync ref
svg_move_target = """                           setDragState({...dragState, isDragging: true});
                        }
                    }"""
svg_move_replacement = """                           setDragState({...dragState, isDragging: true});
                           isDraggingRef.current = true;
                        }
                    }"""
content = content.replace(svg_move_target, svg_move_replacement)

# Edit 4: Update SVG onPointerUp to clear ref after click
svg_up_target = """                  onPointerUp={(e) => {
                    if (dragState) {
                       setDragState(null);
                    }
                  }}"""
svg_up_replacement = """                  onPointerUp={(e) => {
                    if (dragState) {
                       setDragState(null);
                       setTimeout(() => { isDraggingRef.current = false; }, 50);
                    }
                  }}"""
content = content.replace(svg_up_target, svg_up_replacement)

# Edit 5: Update partitions to check isDraggingRef and use correct cursors
h_target = """          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {"""
h_replace = """          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-row-resize hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {"""
content = content.replace(h_target, h_replace)

v_target = """          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-pointer hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {"""
v_replace = """          <g key={pId} 
            className={dragState?.partitionId === pId ? "cursor-grabbing" : "cursor-col-resize hover:opacity-80 transition-opacity"} 
            onPointerDown={(e) => {"""
content = content.replace(v_target, v_replace)

# Edit 6: Fix onClick
click_target = """onClick={(e) => { e.stopPropagation(); togglePartition(pId, idx); }}"""
click_replace = """onClick={(e) => { e.stopPropagation(); if (!isDraggingRef.current) togglePartition(pId, idx); }}"""
content = content.replace(click_target, click_replace)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

