import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("import CustomStorageCalculator from './pages/CustomStorageCalculator';", "import CustomStorageCalculator from './pages/CustomStorageCalculator';\nimport PricingRules from './pages/PricingRules';")

content = content.replace("<Route index element={<Home />} />", "<Route index element={<Home />} />\n            <Route path=\"rules\" element={<PricingRules />} />")

with open('src/App.tsx', 'w') as f:
    f.write(content)
