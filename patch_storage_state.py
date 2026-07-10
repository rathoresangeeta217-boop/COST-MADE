import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

state_vars_old = """  const [activeTab, setActiveTab] = useState<"storage" | "drawer">("storage");"""
state_vars_new = """  const [activeTab, setActiveTab] = useState<"storage" | "drawer">("storage");
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);"""

content = content.replace(state_vars_old, state_vars_new)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
