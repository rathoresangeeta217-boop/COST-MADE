import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_ui = """                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Understructure (Legs)
                  </label>"""

new_ui = """                {!(layout === 'linear' && isHeightAdjustable) && (
                  <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Understructure (Legs)
                  </label>"""
content = content.replace(old_ui, new_ui)

old_ui2 = """                  </div>
                )}
                
                {/* Screens */}"""

new_ui2 = """                  </div>
                )}
                  </>
                )}
                
                {/* Screens */}"""
content = content.replace(old_ui2, new_ui2)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
