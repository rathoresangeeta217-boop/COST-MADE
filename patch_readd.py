import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# Fix parameter declaration
old_param = """  wireManagement,

  flapBoxRate = 450,
  includePedestal,"""
new_param = """  wireManagement,
  flapBoxRate = 450,
  includePedestal,"""
content = content.replace(old_param, new_param)

# Fix history config
old_hist = """      cncDesignOnModesty,
      wireManagement,

  
      includeDrawer,"""
new_hist = """      cncDesignOnModesty,
      wireManagement,
      flapBoxRate,
      includeDrawer,"""
content = content.replace(old_hist, new_hist)

# Fix calculateWorkstationCost main call
old_calc = """      cncDesignOnModesty,
    wireManagement,

    includeDrawer,"""
new_calc = """      cncDesignOnModesty,
    wireManagement,
    flapBoxRate,
    includeDrawer,"""
content = content.replace(old_calc, new_calc)

# Fix line 799-800
old_state = """  const [wireManagement,
 setWireManagement] = useState<string>("raceway"); // 'grommet', 'raceway', 'none'
  const [flapBoxRate, setFlapBoxRate] = useState<number>(450);"""
new_state = """  const [wireManagement, setWireManagement] = useState<string>("raceway"); // 'grommet', 'raceway', 'none'
  const [flapBoxRate, setFlapBoxRate] = useState<number>(450);"""
content = content.replace(old_state, new_state)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
