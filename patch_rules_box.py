import re

with open('src/pages/PricingRules.tsx', 'r') as f:
    content = f.read()

old_block = """            <div>
              <h3 className="font-medium text-gray-900 mb-1">2. Box Legs</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Dimensions:</strong> 600mm × 600mm box.</li>
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">(600 × 4) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>"""

new_block = """            <div>
              <h3 className="font-medium text-gray-900 mb-1">2. Box Base (Conference Table)</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Dimensions:</strong> Calculated as a single large central box.</li>
                <li><strong>Width:</strong> <code className="text-indigo-700">Table Width - 600mm</code></li>
                <li><strong>Depth:</strong> <code className="text-indigo-700">Table Depth - 600mm</code></li>
                <li><strong>Total Area:</strong> <code className="text-indigo-700">((Box Width × 2) + (Box Depth × 2)) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>"""

content = content.replace(old_block, new_block)

with open('src/pages/PricingRules.tsx', 'w') as f:
    f.write(content)
