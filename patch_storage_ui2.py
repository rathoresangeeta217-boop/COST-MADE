import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

quality_html = """            {/* Quality Tier Selection */}"""
quality_html_replacement = """            {/* Construction Category Selection */}
            <div>
              <span className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Construction Category
              </span>
              <div className="grid grid-cols-2 gap-3 mb-4">
                <button
                  type="button"
                  onClick={() => setConstructionCategory("wooden")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "wooden"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Wooden Boards</span>
                </button>
                <button
                  type="button"
                  onClick={() => setConstructionCategory("metal")}
                  className={`p-3 rounded-xl border text-center transition-all ${
                    constructionCategory === "metal"
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium shadow-sm shadow-indigo-100/55"
                      : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="block text-xs font-bold">Metal Construction</span>
                </button>
              </div>
            </div>

            {/* Quality Tier Selection */}"""

content = content.replace(quality_html, quality_html_replacement)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
