from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if self.getpos()[0] == 1430:
                print("Depth at 1430:", self.depth)
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

parser = MyHTMLParser()
parser.feed(text)
