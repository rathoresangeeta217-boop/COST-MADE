import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """        <button
          onClick={() => setActiveTab("drawer")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "drawer"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Single Drawer Calculator
        </button>
      </div>"""

replacement = """        <button
          onClick={() => setActiveTab("drawer")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "drawer"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Single Drawer
        </button>
        <button
          onClick={() => setActiveTab("locker")}
          className={`flex-1 py-2 px-3 text-sm font-medium rounded-lg transition-all ${
            activeTab === "locker"
              ? "bg-white text-indigo-600 shadow-sm border border-gray-200/60"
              : "text-gray-500 hover:text-gray-700 hover:bg-gray-200/50"
          }`}
        >
          Metal Lockers
        </button>
      </div>"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
