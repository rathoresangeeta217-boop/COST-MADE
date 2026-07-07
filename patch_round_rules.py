import re

with open('src/pages/PricingRules.tsx', 'r') as f:
    content = f.read()

old_block = """            <div>
              <h3 className="font-medium text-gray-900 mb-1">3. Round Legs</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">1200mm (circumference) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>"""

new_block = """            <div>
              <h3 className="font-medium text-gray-900 mb-1">3. Round Legs</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Dimensions:</strong> 600mm diameter.</li>
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">1885mm (circumference) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>"""

content = content.replace(old_block, new_block)

with open('src/pages/PricingRules.tsx', 'w') as f:
    f.write(content)
