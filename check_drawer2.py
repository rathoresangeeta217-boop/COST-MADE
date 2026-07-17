from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

lines = text.split('\n')[2530:2935]
fragment = '\n'.join(lines)

parser = MyHTMLParser()
for i, line in enumerate(fragment.split('\n')):
    parser.feed(line + '\n')
    if "</div>" in line or "<div" in line:
        print(f"Line {i+2531}: {line.strip()} (Depth: {parser.depth})")
