with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()
lines = text.split('\n')[2530:2935]
fragment = '\n'.join(lines)
fragment = fragment.replace(r"/\s\([^)]*(mm|Backing)\)$/", "REGEX")
print(repr(fragment[:110]))
