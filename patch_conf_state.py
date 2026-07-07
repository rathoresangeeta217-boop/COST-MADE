import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace("  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);", "  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);\n  const [legCountInput, setLegCountInput] = useState<number>(0);")

content = content.replace("      setAddLeatherlite(editItem.config.addLeatherlite || false);", "      setAddLeatherlite(editItem.config.addLeatherlite || false);\n      setLegCountInput(editItem.config.legCountInput || 0);")

content = content.replace("      addLeatherlite,\n    });", "      addLeatherlite,\n      legCountInput,\n    });")

content = content.replace("    addLeatherlite,\n  ]);", "    addLeatherlite,\n    legCountInput,\n  ]);")

content = content.replace("        addLeatherlite,\n      },", "        addLeatherlite,\n        legCountInput,\n      },")

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
