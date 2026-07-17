import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

# Tags that should be self-closing: rect, input, select (wait, select needs </select>), line, circle
# Wait, select should be closed with </select>.
# Let's see what check_tags2.py reported!

# The report said:
# Unclosed tag: <rect ... rx="2"
# Unclosed tag: <rect ... height="5" fill="#94a3b8" rx="1"
# Unclosed tag: <AnimatedDoorGroup
# Unclosed tag: <line ... strokeWidth="2"
# Unclosed tag: <input ... checked={isCustomSize}
# Unclosed tag: <button type="button"
# Unclosed tag: <select value={boardId}

# Some of these are just line breaks! 
# Like:
# <rect
#   x={...}
#   y={...}
# />
# `check_tags2.py` matched `<rect[^>]*$` on a single line! It just means it didn't find `>` on THAT line!
# That does NOT mean the tag is unclosed, it just means the tag spans multiple lines!
