import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_load = """        if (c.outerMica !== undefined) setOuterMica(c.outerMica);"""
new_load = """        if (c.outerMica !== undefined) setOuterMica(c.outerMica);
        if (c.isHeightAdjustable !== undefined) setIsHeightAdjustable(c.isHeightAdjustable);
        if (c.layout !== undefined) setLayout(c.layout);
        if (c.numPersons !== undefined) setNumPersons(c.numPersons);"""
content = content.replace(old_load, new_load)

old_save = """                          cpuStandType, innerMica, outerMica
                        },"""
new_save = """                          cpuStandType, innerMica, outerMica,
                          isHeightAdjustable, layout, numPersons
                        },"""
content = content.replace(old_save, new_save)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
