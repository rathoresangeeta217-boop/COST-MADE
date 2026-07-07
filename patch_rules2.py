import re

with open('src/pages/PricingRules.tsx', 'r') as f:
    content = f.read()

board_leg_rule = """      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-500" />
          Board Leg ("Same as Table") Calculation
        </h2>
        <div className="space-y-4 text-gray-600">
          <p>When the table uses the same board material for legs, it's calculated based on a 2-slab design.</p>
          <div className="bg-gray-50 p-4 rounded-xl space-y-3">
            <ul className="list-disc list-inside text-sm space-y-2 ml-2">
              <li><strong>Number of Legs:</strong> Fixed at 2 slabs for the understructure.</li>
              <li><strong>Area per Leg:</strong> <code className="text-indigo-700">Depth (mm) × Height (mm)</code></li>
              <li><strong>Total Leg Cost:</strong> <code className="text-indigo-700">Total Area (Sq.Ft) × Board Rate (₹/Sq.Ft)</code></li>
            </ul>
          </div>
        </div>
      </div>"""

new_board_leg_rule = """      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-500" />
          Board Legs Calculation
        </h2>
        <div className="space-y-4 text-gray-600">
          <p>When the table uses the board material for legs, it is calculated based on the leg type:</p>
          <div className="bg-gray-50 p-4 rounded-xl space-y-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-1">1. "Same as Table" (Slab Legs)</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Number of Legs:</strong> Fixed at 2 slabs for the understructure.</li>
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">Depth (mm) × Height (mm)</code></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-1">2. Box Legs</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Dimensions:</strong> 600mm × 600mm box.</li>
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">(600 × 4) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-1">3. Round Legs</h3>
              <ul className="list-disc list-inside text-sm space-y-1 ml-2">
                <li><strong>Area per Leg:</strong> <code className="text-indigo-700">1200mm (circumference) × Height (mm)</code></li>
                <li><strong>Fluted Premium:</strong> Base board rate + ₹100/Sq.Ft.</li>
              </ul>
            </div>
            
            <p className="text-sm mt-3 border-t pt-2 border-gray-200">
              <strong>Total Leg Cost:</strong> <code className="text-indigo-700">Total Area (Sq.Ft) × Adjusted Board Rate (₹/Sq.Ft)</code>
            </p>
          </div>
        </div>
      </div>"""

content = content.replace(board_leg_rule, new_board_leg_rule)

with open('src/pages/PricingRules.tsx', 'w') as f:
    f.write(content)
