from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.root_closed = False
        self.root_closed_line = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.depth == 0 and not self.root_closed:
                self.root_closed = True
                self.root_closed_line = self.getpos()[0]

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

# Only parse lines 593 to 2528
lines = text.split('\n')[592:2528]
fragment = '\n'.join(lines)

parser = MyHTMLParser()
try:
    parser.feed(fragment)
    if parser.root_closed:
        print("Root div was closed at line", parser.root_closed_line + 592)
    print("Final depth:", parser.depth)
except Exception as e:
    print("Error:", e)
