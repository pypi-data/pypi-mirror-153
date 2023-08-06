from html.parser import HTMLParser
class FB2(HTMLParser):
    """ Class of FB2 to txt convertor. Use a feed method to generate a text."""
    book = ""
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        self.book = self.book + data + "\n"
    def finish(self):
        "Generate a book"
        return self.book