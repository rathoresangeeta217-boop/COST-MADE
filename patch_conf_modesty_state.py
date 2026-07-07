import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

state_vars_old = """  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);
  const [legCountInput, setLegCountInput] = useState<number>(0);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);"""

state_vars_new = """  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);
  const [legCountInput, setLegCountInput] = useState<number>(0);
  const [includeModesty, setIncludeModesty] = useState<boolean>(false);
  const [modestyType, setModestyType] = useState<string>("standard");
  const [customModestyHeight, setCustomModestyHeight] = useState<number>(400);
  const [modestyFinish, setModestyFinish] = useState<string>("plain");
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);"""

content = content.replace(state_vars_old, state_vars_new)

effect_old = """      setAddLeatherlite(editItem.config.addLeatherlite || false);
      setLegCountInput(editItem.config.legCountInput || 0);
    }
  }, [editItem]);"""

effect_new = """      setAddLeatherlite(editItem.config.addLeatherlite || false);
      setLegCountInput(editItem.config.legCountInput || 0);
      setIncludeModesty(editItem.config.includeModesty || false);
      setModestyType(editItem.config.modestyType || "standard");
      setCustomModestyHeight(editItem.config.customModestyHeight || 400);
      setModestyFinish(editItem.config.modestyFinish || "plain");
    }
  }, [editItem]);"""

content = content.replace(effect_old, effect_new)

memo_dep_old = """      addLeatherlite,
      legCountInput,
    });
  }, ["""

memo_dep_new = """      addLeatherlite,
      legCountInput,
      includeModesty,
      modestyType,
      customModestyHeight,
      modestyFinish,
    });
  }, ["""

content = content.replace(memo_dep_old, memo_dep_new)

memo_arr_old = """    addLeatherlite,
    legCountInput,
  ]);"""

memo_arr_new = """    addLeatherlite,
    legCountInput,
    includeModesty,
    modestyType,
    customModestyHeight,
    modestyFinish,
  ]);"""

content = content.replace(memo_arr_old, memo_arr_new)

save_old = """        addLeatherlite,
        legCountInput,
      },"""

save_new = """        addLeatherlite,
        legCountInput,
        includeModesty,
        modestyType,
        customModestyHeight,
        modestyFinish,
      },"""

content = content.replace(save_old, save_new)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
