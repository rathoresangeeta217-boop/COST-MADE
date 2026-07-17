import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# 1. Add state variables
state_target = """  const [lockerBoxHeight, setLockerBoxHeight] = useState<number>(300);
  const [removedLockerDoors, setRemovedLockerDoors] = useState<string[]>([]);"""

state_replace = """  const [lockerBoxHeight, setLockerBoxHeight] = useState<number>(300);
  const [removedLockerDoors, setRemovedLockerDoors] = useState<string[]>([]);
  const [lockerLockType, setLockerLockType] = useState<"cam" | "digital" | "padlock" | "none">("cam");
  const [lockerCncDesign, setLockerCncDesign] = useState<boolean>(false);"""

content = content.replace(state_target, state_replace, 1)

# 2. Add options to UI
ui_target = """              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Thickness (CRCA Sheet)</label>
                  <select"""

ui_replace = """              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Lock Type</label>
                  <select
                    value={lockerLockType}
                    onChange={(e) => setLockerLockType(e.target.value as "cam" | "digital" | "padlock" | "none")}
                    className="w-full px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none font-medium"
                  >
                    <option value="none">None</option>
                    <option value="cam">Cam Lock</option>
                    <option value="padlock">Padlock Hasp</option>
                    <option value="digital">Digital / RFID Lock</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">CNC Design (Louvers / Perforation)</label>
                  <label className="flex items-center gap-2 mt-2 cursor-pointer">
                    <input type="checkbox" checked={lockerCncDesign} onChange={(e) => setLockerCncDesign(e.target.checked)} className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
                    <span className="text-sm font-medium text-gray-700">Add CNC Cutout</span>
                  </label>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Thickness (CRCA Sheet)</label>
                  <select"""

content = content.replace(ui_target, ui_replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

