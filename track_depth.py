from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.log = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if 'className' in dict(attrs) and 'xl:col-span-5' in dict(attrs)['className']:
                self.log.append((self.getpos()[0], f"+ RIGHT SIDE START depth={self.depth}"))
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if len(self.log) > 0 and self.depth == int(self.log[-1][1].split('=')[1]):
                self.log.append((self.getpos()[0], f"- RIGHT SIDE END depth={self.depth}"))
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

parser = MyHTMLParser()
parser.feed(text)

for l in parser.log:
    print(l)
