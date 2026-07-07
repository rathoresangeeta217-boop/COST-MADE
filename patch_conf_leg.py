import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# Update signature
content = content.replace("  addLeatherlite,\n}: any) {", "  addLeatherlite,\n  legCountInput,\n}: any) {")

# Replace legCount definition
content = content.replace("  let legCount = mainWidth >= 2400 ? 3 : 2;", "  let legCount = legCountInput || (mainWidth >= 2400 ? 3 : 2);")

# Update state variables
state_vars = """  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);"""
new_state_vars = """  const [addLeatherlite, setAddLeatherlite] = useState<boolean>(false);
  const [legCount, setLegCount] = useState<number>(0);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);"""
content = content.replace(state_vars, new_state_vars)

# Update editItem effect
edit_item = """      setAddLeatherlite(editItem.config.addLeatherlite || false);"""
new_edit_item = """      setAddLeatherlite(editItem.config.addLeatherlite || false);
      setLegCount(editItem.config.legCount || 0);"""
content = content.replace(edit_item, new_edit_item)

# Update width effect for auto leg count
width_effect = """  useEffect(() => {
    if (editItemId) return;
    // auto update logic? No, let's just make the user choose
  }, []); // this is fake"""
  
# Instead of doing an effect for width, just let legCount defaults to 0 (auto).
# If 0, UI shows "Auto (2/3)" or something. Or we just set it based on width if they don't touch it. 
# Better: just add a dropdown for Leg Count in UI.

ui_input = """                <Select value={legType} onValueChange={setLegType}>
                  <SelectTrigger className="mt-1.5 w-full bg-white shadow-sm border-gray-200 focus:ring-indigo-500 focus:border-indigo-500 rounded-xl">
                    <SelectValue placeholder="Select legs" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectLabel>Metal Frames</SelectLabel>
                      <option value="metal_straight">Straight Legs</option>
                      <option value="metal_u">U-Shape Legs</option>"""
                      
# Wait, it's using <SelectItem> not <option> inside SelectContent?
