import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Let's fix the duplicated getPieceRate in calcData
good_start = """  const calcData = useMemo(() => {
    const mainThk = constructionCategory === 'metal' ? angleThickness : boardThickness;
    const shelfThk = constructionCategory === 'metal' ? (shelfMaterialType === 'wooden' ? woodenShelfThickness : angleThickness) : boardThickness;
    const shelfBoardId = constructionCategory === 'metal' && shelfMaterialType === 'wooden' ? woodenShelfId : boardId;
    
    const getPieceRate = (label: string, defaultThickness: number, overrideBid?: string) => {
        const key = label.replace(/\s\([^)]*(mm|Backing)\)$/, '');
        const overrideBoardId = pieceOverrides[key];
        const overrideThickness = thicknessOverrides[key];
        
        const bid = overrideBoardId && overrideBoardId !== 'default' ? overrideBoardId : (overrideBid || boardId);
        const thk = overrideThickness || defaultThickness;
        const b = boards.find(b => b.id === bid) || getBoards(quality, 'wooden').find(b => b.id === bid);
        if (!b) return 100;
        return getBoardRate(bid, b.costPerSqFt, thk, quality);
    };"""

content = re.sub(
    r'const calcData = useMemo\(\(\) => \{.*?(?=\s*let angularShelvesCost = 0;)',
    good_start.replace('\\', '\\\\'),
    content,
    flags=re.DOTALL
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
