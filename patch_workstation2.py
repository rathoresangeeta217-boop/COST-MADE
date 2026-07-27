import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_state = """  const [layout, setLayout] = useState<string>("linear"); // 'linear', 'back_to_back'"""
new_state = """  const [layout, setLayout] = useState<string>("linear"); // 'linear', 'back_to_back'
  const [isHeightAdjustable, setIsHeightAdjustable] = useState<boolean>(false);"""
content = content.replace(old_state, new_state)

old_dep = """      topMaterialCategory,
      marbleTypeId,
    });
  }, ["""
new_dep = """      topMaterialCategory,
      marbleTypeId,
      isHeightAdjustable,
    });
  }, ["""
content = content.replace(old_dep, new_dep)

old_dep_arr = """    topMaterialCategory,
    marbleTypeId,
  ]);"""
new_dep_arr = """    topMaterialCategory,
    marbleTypeId,
    isHeightAdjustable,
  ]);"""
content = content.replace(old_dep_arr, new_dep_arr)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
