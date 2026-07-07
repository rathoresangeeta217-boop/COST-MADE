with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<option value="1_drawer_1_shutter">1 drawer at top + Shutter below</option>',
    '<option value="1_drawer_1_shutter">1 drawer at top + Shutter below</option>\n                        <option value="vertical_horizontal">Vertical Bay with Horizontal</option>'
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
