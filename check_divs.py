from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.log = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if 'className' in dict(attrs):
                self.log.append((self.getpos()[0], f"+ <div className=\"{dict(attrs)['className']}\"> depth={self.depth}"))
            else:
                self.log.append((self.getpos()[0], f"+ <div> depth={self.depth}"))
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.log.append((self.getpos()[0], f"- </div> depth={self.depth}"))
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

lines = text.split('\n')
for idx, line in enumerate(lines):
    if "Right Side:" in line:
        start_idx = idx
        break

fragment = '\n'.join(lines[start_idx:start_idx+1500])
parser = MyHTMLParser()
parser.feed(fragment)

for l in parser.log:
    if l[0] > 1000 and l[0] < 1200:
        print(l)
