import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

# Just a simple count of quotes in the file
print(f"Double quotes: {content.count('\"')}")
print(f"Single quotes: {content.count(\"'\")}")
print(f"Backticks: {content.count('`')}")
