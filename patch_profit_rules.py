import re

with open('src/pages/PricingRules.tsx', 'r') as f:
    content = f.read()

old_block = """            <li><strong>Tooling Cost:</strong> Fixed addition (e.g., ₹100).</li>
            <li><strong>Profit Margin:</strong> A fixed percentage (e.g., 25%) applied on top of the total material, labor, packing, and tooling costs combined.</li>"""

new_block = """            <li><strong>Tooling Cost:</strong> Fixed addition (e.g., ₹100).</li>
            <li><strong>Profit Margin:</strong> A fixed percentage applied on top of the total material, labor, packing, and tooling costs combined. (Generally 25%, but 40% when Fluted Box Legs are selected).</li>"""

content = content.replace(old_block, new_block)

with open('src/pages/PricingRules.tsx', 'w') as f:
    f.write(content)
