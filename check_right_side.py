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
            if self.depth < 0:
                print(f"Negative depth at line {self.getpos()[0] + 1429}")
                # Reset to 0 so we can keep finding them
                self.depth = 0

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

lines = text.split('\n')[1429:2528]
fragment = '\n'.join(lines)

parser = MyHTMLParser()
parser.feed(fragment)
print("Final depth:", parser.depth)
