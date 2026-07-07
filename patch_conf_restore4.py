import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

missing_part = """          </div>
        </div>
        
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden sticky top-6">
            <div className="bg-gray-900 p-6 text-white">
              <h2 className="text-xl font-semibold mb-2">Cost Summary</h2>
              <p className="text-gray-400 text-sm">Estimated manufacturing cost</p>
            </div>
            <div className="p-6 space-y-6">
              {/* Board Details */}
              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm font-semibold text-gray-900 border-b pb-2">
                  <span>Board Material</span>
                  <span>₹{costSummary.boardCostTotal.toLocaleString()}</span>
                </div>
                <div className="space-y-2">
                  {costSummary.boardPiecesDetails.map((item: any, idx: number) => (
                    <div key={idx} className="flex justify-between text-sm text-gray-500">
                      <span className="pr-4">{item.label}</span>
                      <span className="whitespace-nowrap">₹{item.cost.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Hardware Details */}"""

content = content.replace("            </section>\n              {/* Hardware Details */}", "            </section>\n" + missing_part)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
