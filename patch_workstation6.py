import re
with open('src/pages/WorkstationCalculator.tsx', 'r') as f:
    content = f.read()

old_ui = """                      </select>
                    </div>
                  </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Front Partition Screen
                </label>"""

new_ui = """                      </select>
                    </div>
                  </>
                )}
                </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Front Partition Screen
                </label>"""
content = content.replace(old_ui, new_ui)

with open('src/pages/WorkstationCalculator.tsx', 'w') as f:
    f.write(content)
