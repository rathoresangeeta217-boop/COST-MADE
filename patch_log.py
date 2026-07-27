import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

old_log = """      const calcData = useMemo(() => {
    const mainThk = constructionCategory === 'metal' ? angleThickness : boardThickness;"""

new_log = """      const calcData = useMemo(() => {
    const mainThk = constructionCategory === 'metal' ? angleThickness : boardThickness;
    console.log(`calcData running... constructionCategory: ${constructionCategory}, angleThickness: ${angleThickness}, boardId: ${boardId}`);"""

content = content.replace(old_log, new_log)
with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
