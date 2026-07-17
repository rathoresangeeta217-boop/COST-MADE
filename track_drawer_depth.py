from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.log = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if self.getpos()[0] >= 2583:
                self.log.append((self.getpos()[0], f"+ depth={self.depth}"))
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.getpos()[0] >= 2583:
                self.log.append((self.getpos()[0], f"- depth={self.depth}"))
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

parser = MyHTMLParser()
parser.feed(text)

print(f"Final depth after parsing: {parser.depth}")

# We want to see where depth drops below 1 for the first time inside storage
for l in parser.log:
    if "depth=1" in l[1] and "-" in l[1]:
        print("Dropped to 0 at:", l)
