with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    text = f.read()

# Let's write a simple HTML parser to track opening and closing divs
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.div_stack = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.div_stack.append(self.getpos()[0])
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_stack:
                self.div_stack.pop()
            else:
                print(f"Extra closing div at line {self.getpos()[0]}")

parser = MyHTMLParser()
# Wait, HTML parser will choke on JSX like <div {...props}>
try:
    parser.feed(text)
    print("Unclosed divs opened at lines:", parser.div_stack)
except Exception as e:
    print("Error parsing:", e)
