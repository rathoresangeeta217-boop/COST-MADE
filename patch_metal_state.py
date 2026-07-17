import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

new_states = """  const [constructionCategory, setConstructionCategory] = useState<"wooden" | "metal">("wooden");
  const [angleThickness, setAngleThickness] = useState<number>(1.6);
  const [shelfMaterialType, setShelfMaterialType] = useState<"metal" | "wooden">("metal");
  const [woodenShelfId, setWoodenShelfId] = useState<string>("plpb");
  const [woodenShelfThickness, setWoodenShelfThickness] = useState<number>(18);
  const [addVerticalPartitionMiddle, setAddVerticalPartitionMiddle] = useState<boolean>(false);
"""

content = content.replace('  const [constructionCategory, setConstructionCategory] = useState<"wooden" | "metal">("wooden");\n', new_states)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
