import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Extract the storage tab block
m = re.search(r'\{activeTab === "storage" && \((.*?)\)\}\n\n      \{activeTab === "drawer"', content, flags=re.DOTALL)
if m:
    storage_content = m.group(1)
    
    # Strip comments to not count them
    storage_content = re.sub(r'\{/\*.*?\*/\}', '', storage_content, flags=re.DOTALL)
    
    open_divs = len(re.findall(r'<div\b', storage_content))
    close_divs = len(re.findall(r'</div\b', storage_content))
    
    print(f"Open divs: {open_divs}, Close divs: {close_divs}")
else:
    print("Could not find storage tab block")
