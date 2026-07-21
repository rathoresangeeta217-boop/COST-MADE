import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_back = """    // Back Panel
    const backPanelThk = 6; // default back panel thickness
    addPiece("Back Panel", width, height, 1, backPanelThk);"""

new_back = """    // Back Panel
    const backPanelThk = constructionCategory === 'metal' ? mainThk : 6;
    addPiece("Back Panel", width, height, 1, backPanelThk);"""

content = content.replace(old_back, new_back)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
