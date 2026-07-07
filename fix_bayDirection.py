import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'const [numBays, setNumBays] = useState<number>(3);',
    'const [bayDirection, setBayDirection] = useState<\'vertical\' | \'horizontal\'>(\'vertical\');\n  const [numBays, setNumBays] = useState<number>(3);'
)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)
print("Done")
