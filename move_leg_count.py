import re

with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

# First, extract the block we added
block_start = '              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">\n                <div>\n                  <label className="block text-sm font-medium text-gray-700 mb-1">\n                    Number of Leg Panels / Frames\n                  </label>'

if block_start in content:
    start_idx = content.find('              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">\n                <div>\n                  <label className="block text-sm font-medium text-gray-700 mb-1">\n                    Number of Leg Panels / Frames\n                  </label>')
    end_idx = content.find('                </div>\n              </div>', start_idx) + len('                </div>\n              </div>')
    
    block_content = content[start_idx:end_idx]
    
    # Remove it from the current location
    content = content[:start_idx] + content[end_idx:]
    
    # Now find where to insert it, right after the Understructure block (around line 1600)
    insert_target = '                {legId === "metal_leg" && (\n                  <>\n                    <div className="sm:col-span-2">\n                      <label className="block text-sm font-medium text-gray-700 mb-1">\n                        Metal Pipe Size\n                      </label>'
    
    if insert_target in content:
        # Actually, let's insert it before the Understructure select
        insert_target2 = '                <div>\n                  <label className="block text-sm font-medium text-gray-700 mb-1">\n                    Understructure (Legs)\n                  </label>'
        
        # Or even better, just replace the block content to be a simple div, and insert it
        new_block = """                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Leg Panels / Frames
                  </label>
                  <input
                    type="number"
                    value={legCountOverride === 0 ? '' : legCountOverride}
                    onChange={(e) => setLegCountOverride(Number(e.target.value) || 0)}
                    placeholder="Auto (based on layout)"
                    className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all outline-none"
                    min="0"
                  />
                </div>"""
        
        content = content.replace(insert_target2, new_block + '\n' + insert_target2)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
