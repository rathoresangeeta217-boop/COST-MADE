with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
    
# Let's count <div> and </div>
lines = text.split('\n')
div_count = 0
for i, line in enumerate(lines):
    if '<div' in line:
        div_count += line.count('<div')
    if '</div' in line:
        div_count -= line.count('</div')
    
print("Final div balance:", div_count)
