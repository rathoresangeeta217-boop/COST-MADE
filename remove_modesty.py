import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Remove state variables
content = re.sub(r'\s*const \[includeModesty, setIncludeModesty\] = useState<boolean>\(.*?;\n\s*const \[modestyType, setModestyType\] = useState<string>\(.*?;', '', content)

# 2. Remove editItem assignment
content = re.sub(r'\s*if \(editItem\.config\.includeModesty !== undefined\) \{.*?\n\s*\}\n\s*if \(editItem\.config\.modestyType\) \{.*?\n\s*\}', '', content, flags=re.DOTALL)

# 3. Remove calculation
calc_regex = r'\s*// Modesty Panel\s*if \(includeModesty\) \{.*?\n\s*\}'
content = re.sub(calc_regex, '', content, flags=re.DOTALL)

# 4. Remove from parameters of calculateConferenceCost
content = re.sub(r'\s*includeModesty,\n\s*modestyType,', '', content)

# 5. Remove from UI
ui_regex = r'\s*\{\/\* Modesty Panel \*\/}\s*<section>.*?</section>'
content = re.sub(ui_regex, '', content, flags=re.DOTALL)

# 6. Remove from exports (PDF and Excel)
content = re.sub(r'\s*\["Modesty Panel", includeModesty \? \(modestyType === "full" \? "Full Height \(715mm\)" : "Standard \(400mm\)"\) : "None"\],', '', content)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
