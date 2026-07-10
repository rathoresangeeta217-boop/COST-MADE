import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

btn = """        <div className="flex gap-2">
          <button
            onClick={copyImagePrompt}
            className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-xl hover:bg-indigo-100/80 hover:border-indigo-200 transition-all shadow-sm"
          >
            <Copy className="w-4 h-4 text-indigo-600" />
            {copiedPrompt ? "Copied!" : "Image Prompt"}
          </button>
          <button"""

content = content.replace("""        <div className="flex gap-2">
          <button""", btn)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
