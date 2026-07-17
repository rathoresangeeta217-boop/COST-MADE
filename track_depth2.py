from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.targets = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if 'className' in dict(attrs) and 'xl:col-span-5' in dict(attrs)['className']:
                self.targets.append(self.depth)
                print(f"Start at line {self.getpos()[0]}, depth {self.depth}")
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.depth in self.targets:
                print(f"End at line {self.getpos()[0]}, depth {self.depth}")
                self.targets.remove(self.depth)
            self.depth -= 1

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

parser = MyHTMLParser()
parser.feed(text)
