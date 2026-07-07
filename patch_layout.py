import re

with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

old_import = """import { Pickaxe, Home, LogIn, LogOut, Cloud } from 'lucide-react';"""
new_import = """import { Pickaxe, Home, LogIn, LogOut, Cloud, FileDown } from 'lucide-react';\nimport { downloadHardwarePdf } from '../lib/downloadHardwarePdf';"""
content = content.replace(old_import, new_import)

old_nav = """            <Link
              to="/rules"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Pickaxe className="w-4 h-4" />
              Pricing Rules
            </Link>
            
            <div className="w-px h-6 bg-gray-200"></div>"""
new_nav = """            <Link
              to="/rules"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Pickaxe className="w-4 h-4" />
              Pricing Rules
            </Link>
            
            <button
              onClick={downloadHardwarePdf}
              className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors bg-indigo-50 px-3 py-1.5 rounded-md"
            >
              <FileDown className="w-4 h-4" />
              Hardware Rates
            </button>

            <div className="w-px h-6 bg-gray-200"></div>"""
content = content.replace(old_nav, new_nav)

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)
