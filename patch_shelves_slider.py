with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '["open", "shutter_solid", "shutter_glass", "shutters_double", "1_drawer_open", "1_drawer_1_shutter"].includes(bay.style)',
    '["open", "shutter_solid", "shutter_glass", "shutters_double", "1_drawer_open", "1_drawer_1_shutter", "vertical_horizontal"].includes(bay.style)'
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
