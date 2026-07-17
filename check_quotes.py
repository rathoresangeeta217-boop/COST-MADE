with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

# remove regex
text = text.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")

print("Single:", text.count("'"))
print("Double:", text.count('"'))
print("Backtick:", text.count('`'))
