with open('src/types.ts', 'r') as f:
    content = f.read()

new_product = """  {
    id: 'conference_table',
    name: 'Conference Table',
    description: 'Calculate manufacturing and material costs for Conference tables.',
    imageUrl: 'https://images.unsplash.com/photo-1570126618953-d437176e8c79?auto=format&fit=crop&q=80&w=800',
    path: '/calculator/conference-table',
  },
"""
content = content.replace("];", new_product + "];")

with open('src/types.ts', 'w') as f:
    f.write(content)
print("Done")
