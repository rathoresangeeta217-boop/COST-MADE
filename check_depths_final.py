from html.parser import HTMLParser
import sys

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

lines = text.split('\n')
parser = MyHTMLParser()

print("Tracking from line 1430:")
for i, line in enumerate(lines):
    parser.feed(line + '\n')
    if i >= 1429 and i <= 2530:
        if "<div" in line or "</div" in line:
            print(f"Line {i+1}: {line.strip()} (Depth: {parser.depth})")
