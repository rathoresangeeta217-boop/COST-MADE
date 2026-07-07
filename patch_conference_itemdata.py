import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_config = """      config: {
        mainWidth,
        mainDepth,
        height,
        topThickness,
        boardId,
        quality,
        legType,
        wireManagement,
        addLeatherlite,
      },"""

new_config = """      config: {
        mainWidth,
        mainDepth,
        height,
        topThickness,
        boardId,
        quality,
        legType,
        wireManagement,
        addLeatherlite,
        includeModesty,
        modestyType,
      },"""

content = content.replace(old_config, new_config)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
