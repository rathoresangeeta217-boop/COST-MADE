import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# I need to fix the closing of the JSX block.
# Right now we have:
#            </div>
#          </div>
#            )}
#
#          {/* Section 3: Detailed Cutting piece specifications list */}

# The `)}` should be before `</div>` that closes Section 2, because `{constructionCategory === "metal" ? ( ... ) : ( ... )}` is inside `<div>`.
content = content.replace(
    "          </div>\n\n            )}\n\n          {/* Section 3",
    "            )}\n          </div>\n\n          {/* Section 3"
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
