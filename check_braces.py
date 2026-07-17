with open('backup.tsx', 'r') as f:
    text = f.read()

print("Total {:", text.count('{'))
print("Total }:", text.count('}'))
print("Total (:", text.count('('))
print("Total ):", text.count(')'))
