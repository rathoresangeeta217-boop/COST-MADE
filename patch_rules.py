import re

with open('src/pages/PricingRules.tsx', 'r') as f:
    content = f.read()

content = content.replace("Buffers (₹7/pc), Nuts (₹5/pc), Butterfly brackets (₹12.5/pc).", "Buffers (₹7/pc), Nuts (₹5/pc), Butterfly brackets (₹12.5/pc), Clamps (₹10/pc).")

with open('src/pages/PricingRules.tsx', 'w') as f:
    f.write(content)
