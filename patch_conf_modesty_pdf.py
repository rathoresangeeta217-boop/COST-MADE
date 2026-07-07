import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

pdf_modesty = """        ["Leg Type", legType.replace("_", " ").toUpperCase()],
        ["Modesty Panel", includeModesty ? `Yes - ${modestyType} (${modestyFinish})` : "No"],"""
content = content.replace('        ["Leg Type", legType.replace("_", " ").toUpperCase()],', pdf_modesty)

excel_modesty = """      ["Leg Type", legType.replace("_", " ").toUpperCase()],
      ["Modesty Panel", includeModesty ? `Yes - ${modestyType} (${modestyFinish})` : "No"],"""
content = content.replace('      ["Leg Type", legType.replace("_", " ").toUpperCase()],', excel_modesty)

prompt_modesty = """const modestyDesc = includeModesty ? ` It features a ${modestyFinish} modesty panel.` : "";
    const prompt = `A highly realistic, professional product photography studio shot of a modern conference table. The table has a dimension of ${mainWidth}mm width and ${mainDepth}mm depth. 
It features a ${topThickness}mm thick ${boardId.replace('_', ' ')} finish top. 
The base consists of ${legType.replace('_', ' ')} legs.${modestyDesc}"""
content = content.replace('The base consists of ${legType.replace(\'_\', \' \')} legs.\\n', prompt_modesty)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
