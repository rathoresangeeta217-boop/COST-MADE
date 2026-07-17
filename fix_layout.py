import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Edit 1: Remove the premature closing div
target1 = """              </svg>
              )}
              </div>
            </div>
          </div>

          {/* Section 5: Estimated Custom Quote Pricing breakdown card */}"""

replacement1 = """              </svg>
              )}
              </div>
            </div>

          {/* Section 5: Estimated Custom Quote Pricing breakdown card */}"""

content = content.replace(target1, replacement1, 1)

# Edit 2: Add the closing div back before the end of the grid
target2 = """              </table>
            </div>
          </div>

        </div>"""

replacement2 = """              </table>
            </div>
          </div>
        </div>

        </div>"""

content = content.replace(target2, replacement2, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

