import re

with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

nav_link = """            <Link
              to="/"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Home className="w-4 h-4" />
              Products
            </Link>"""

new_nav_link = nav_link + """
            <Link
              to="/rules"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Pickaxe className="w-4 h-4" />
              Pricing Rules
            </Link>"""

content = content.replace(nav_link, new_nav_link)

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)
