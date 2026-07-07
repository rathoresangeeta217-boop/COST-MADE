import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Update calculateConferenceCost parameters
old_params = """export function calculateConferenceCost({
  mainWidth,
  mainDepth,
  height,
  topThickness,
  boardId,
  quality,
  legType,
  wireManagement,
  addLeatherlite,
}: any) {"""

new_params = """export function calculateConferenceCost({
  mainWidth,
  mainDepth,
  height,
  topThickness,
  boardId,
  quality,
  legType,
  wireManagement,
  addLeatherlite,
  includeModesty,
  modestyType,
}: any) {"""

content = content.replace(old_params, new_params)

# 2. Update useMemo
old_memo = """  const costSummary = useMemo(() => {
    return calculateConferenceCost({
      mainWidth,
      mainDepth,
      height,
      topThickness,
      boardId,
      quality,
      legType,
      wireManagement,
      addLeatherlite,
    });
  }, [
    mainWidth,
    mainDepth,
    height,
    topThickness,
    boardId,
    quality,
    legType,
    wireManagement,
    addLeatherlite,
  ]);"""

new_memo = """  const costSummary = useMemo(() => {
    return calculateConferenceCost({
      mainWidth,
      mainDepth,
      height,
      topThickness,
      boardId,
      quality,
      legType,
      wireManagement,
      addLeatherlite,
      includeModesty,
      modestyType,
    });
  }, [
    mainWidth,
    mainDepth,
    height,
    topThickness,
    boardId,
    quality,
    legType,
    wireManagement,
    addLeatherlite,
    includeModesty,
    modestyType,
  ]);"""

content = content.replace(old_memo, new_memo)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
