import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Fix the inner metal SVG
content = content.replace(
"""                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>
              )}
              ) : (
                <svg""", 
"""                   <text x={width / 2} y="-20" fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold">{width}mm</text>
                   <text x="-20" y={height / 2} fill="#64748b" fontSize="24" textAnchor="middle" fontWeight="bold" transform={`rotate(-90 -20 ${height/2})`}>{height}mm</text>
                 </svg>
              ) : (
                <svg""")


# Fix the other SVG closures that got `)}` erroneously
content = content.replace("              </svg>\n              )}", "              </svg>")

# Wait, the first one SHOULD have `)}` at the end of the wooden SVG block
# The wooden SVG block ends around 3520. Let's see.
# The original file had the SVG block ending and then `</div>` of the `flex justify-center` container.
# Then the `</div>` of Section 4.
# Then Section 5.
# Let's restore the `)}` for the wooden SVG block, because it is the `) : (` block closure.

content = content.replace("""                  })()
                )}
              </svg>
              </div>""", """                  })()
                )}
              </svg>
              )}
              </div>""")

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
