from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.log = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            self.log.append((self.getpos()[0], f"+ depth={self.depth}"))
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.log.append((self.getpos()[0], f"- depth={self.depth}"))
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

# Only parse lines 1483 to 2485
lines = text.split('\n')
fragment = '\n'.join(lines[1482:2485])

parser = MyHTMLParser()
parser.feed(fragment)

for l in parser.log:
    print(l)
