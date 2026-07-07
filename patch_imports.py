import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

lucide_imports = re.search(r'import \{(.*?)\} from "lucide-react";', content, re.DOTALL)
if lucide_imports:
    imports = lucide_imports.group(1).split(',')
    imports = [i.strip() for i in imports if i.strip()]
    for icon in ['Download', 'FileSpreadsheet', 'Copy', 'IndianRupee']:
        if icon not in imports:
            imports.append(icon)
    new_lucide_import = "import {\n  " + ",\n  ".join(imports) + "\n} from \"lucide-react\";"
    content = content.replace(lucide_imports.group(0), new_lucide_import)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
