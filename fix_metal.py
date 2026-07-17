import re
with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# I want to close the metal vs wooden branches correctly!
# The false (wooden) branch starts at 2202 with `<>`.
# It SHOULD wrap BOTH the grid controls AND the Individual Bay configurator cards!
# So the `<>` should close at 2468, where I added `</>\n )}`.

# First, let's remove the extra `</div>` at 2246.
content = content.replace(
"""                  </div>
                </div>
              </div>
            </div>

            {/* Individual Bay configurator cards */}""",
"""                  </div>
                </div>
              </div>

            {/* Individual Bay configurator cards */}"""
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
