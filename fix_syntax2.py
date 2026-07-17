import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("                 </svg>\n              )}\n              ) : (\n                <svg", "                 </svg>\n              ) : (\n                <svg")

# The second `</svg>` (the wooden one) also got an extra `)}` if it was replaced globally, or maybe the other ones.
# Actually, the python script did:
# content = re.sub(r'              <\/svg>', r'              </svg>\n              )}', content)
# This would replace ANY `              </svg>` with the extra `)}`

# Let's see how many `              </svg>\n              )}` there are.
# Wait, let's just fix the single drawer one too. It might have broken.
