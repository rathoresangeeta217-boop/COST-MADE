import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

m = re.search(r'\{activeTab === "storage" && \((.*?)\)\}\n\n      \{activeTab === "drawer"', content, flags=re.DOTALL)
if m:
    storage_content = m.group(1)
    # let's strip comments
    storage_content = re.sub(r'\{/\*.*?\*/\}', '', storage_content, flags=re.DOTALL)
    
    # Let's count unescaped ( and )
    open_p = storage_content.count('(')
    close_p = storage_content.count(')')
    print(f"Open (: {open_p}, Close ): {close_p}")
