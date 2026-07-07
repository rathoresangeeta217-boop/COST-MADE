const fs = require('fs');
let file = 'src/pages/CustomStorageCalculator.tsx';
let content = fs.readFileSync(file, 'utf8');

const target = `              {/* Board Material and Thickness Selection */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">`;

const replacement = `              {/* Quality Tier Selection */}
              <div className="pt-4 border-t border-gray-100">
                <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Quality Tier Selection
                </span>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setQuality("standard")}
                    className={\`p-3 rounded-xl border text-center transition-all \${
                      quality === "standard"
                        ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                        : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                    }\`}
                  >
                    <span className="block text-xs font-bold">Standard Quality</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuality("affordable")}
                    className={\`p-3 rounded-xl border text-center transition-all \${
                      quality === "affordable"
                        ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                        : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                    }\`}
                  >
                    <span className="block text-xs font-bold">Affordable Quality</span>
                  </button>
                </div>
              </div>
              
              {/* Board Material and Thickness Selection */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-gray-100">`;

if (content.includes(target)) {
  content = content.replace(target, replacement);
  fs.writeFileSync(file, content);
  console.log("Patched CustomStorageCalculator.tsx with quality");
} else {
  console.log("Could not find target for quality patch");
}
