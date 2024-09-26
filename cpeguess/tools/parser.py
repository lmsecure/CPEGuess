import cpeguess.tools.handler as handler
import xml.sax


class XMLParser:
    def __init__(self, path, handler):
        self.parser = xml.sax.make_parser()
        self.handler = handler
        self.path = path
        self.parser.setContentHandler(self.handler)

    def parse(self):
        self.parser.parse(self.path)
        return self.handler.result

    @classmethod
    def for_handler(cls, path:str, handler):
        return cls(path=path, handler=handler)
