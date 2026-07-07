import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

old_edit = """      setLegType(editItem.config.legType || "metal_straight");
      setWireManagement(editItem.config.wireManagement || "none");
      setAddLeatherlite(editItem.config.addLeatherlite || false);
    }
  }, [editItem]);"""

new_edit = """      setLegType(editItem.config.legType || "metal_straight");
      setWireManagement(editItem.config.wireManagement || "none");
      setAddLeatherlite(editItem.config.addLeatherlite || false);
      if (editItem.config.includeModesty !== undefined) {
          setIncludeModesty(editItem.config.includeModesty);
      }
      if (editItem.config.modestyType) {
          setModestyType(editItem.config.modestyType);
      }
    }
  }, [editItem]);"""

content = content.replace(old_edit, new_edit)

with open('src/pages/ConferenceTableCalculator.tsx', 'w') as f:
    f.write(content)
