from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if self.getpos()[0] == 2866:
                print("Depth at 2866:", self.depth)
            
    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.depth == 2 and self.getpos()[0] >= 2866 and self.getpos()[0] <= 3660:
                print(f"Depth hit 2 at line {self.getpos()[0]}")

with open('backup.tsx', 'r') as f:
    text = f.read()

parser = MyHTMLParser()
parser.feed(text)
