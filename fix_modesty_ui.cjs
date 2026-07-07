const fs = require('fs');

const files = ['src/pages/WorkstationCalculator.tsx', 'src/pages/LShapeTableCalculator.tsx'];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');

  // Fix LShape and Workstation modesty Finish dropdown
  const target = `                          <option value="shorter">Shorter (300 mm)</option>
                        </select>
                      </div>`;
                      
  const replacement = `                          <option value="shorter">Shorter (300 mm)</option>
                        </select>
                        <select
                          value={modestyFinish}
                          onChange={(e) => setModestyFinish(e.target.value)}
                          className="block w-full max-w-xs px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-md text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                          <option value="plain">Plain</option>
                          <option value="fluted">Fluted</option>
                        </select>
                      </div>`;
                      
  if (content.includes(target)) {
     content = content.replace(target, replacement);
     fs.writeFileSync(file, content);
     console.log("Patched " + file);
  } else {
     console.log("Could not find target in " + file);
  }
}
