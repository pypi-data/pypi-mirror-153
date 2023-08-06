from html.parser import HTMLParser
class rss(HTMLParser):
    """ Class of rss to txt convertor. Use a feed method to generate a text."""
    rss = ""
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        self.rss = self.rss + data + "\n"
    def unknown_decl(self, data):
        if type(data) is str:
            self.rss = self.rss + data + "\n"
    def finish(self):
        "Generate a str object"
        return self.rss