import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("<Switch checked={addLeatherlite} onCheckedChange={setAddLeatherlite} />", """<input 
                    type="checkbox" 
                    checked={addLeatherlite} 
                    onChange={(e) => setAddLeatherlite(e.target.checked)}
                    className="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer"
                  />""")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
