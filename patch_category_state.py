import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'const [quality, setQuality] = useState<string>("standard");',
    'const [constructionCategory, setConstructionCategory] = useState<"wooden" | "metal">("wooden");\n  const [quality, setQuality] = useState<string>("standard");'
)

content = content.replace(
    'const boards = useMemo(() => getBoards(quality), [quality]);',
    'const boards = useMemo(() => getBoards(quality, constructionCategory), [quality, constructionCategory]);\n  useEffect(() => {\n    setBoardId(boards[0].id);\n    setBoardThickness(getAvailableThicknesses(boards[0].id, quality)[0]);\n  }, [boards, quality]);'
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
