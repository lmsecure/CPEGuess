import xml.sax
import time

class CPEHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.cpe = ""
        self.title = ""
        self.title_seen = False
        self.cpe = ""
        self.record = {}
        self.refs = []
        self.itemcount = 0
        self.wordcount = 0
        self.start_time = time.time()
        self.result = set()

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "cpe-23:cpe23-item":
            self.record["cpe-23"] = attributes["name"]
        if tag == "title":
            self.title_seen = True
        if tag == "reference":
            self.refs.append(attributes["href"])

    def characters(self, data):
        if self.title_seen:
            self.title = self.title + data

    def endElement(self, tag):
        if tag == "title":
            self.record["title"] = self.title
            self.title = ""
            self.title_seen = False
        if tag == "references":
            self.record["refs"] = self.refs
            self.refs = []
        if tag == "cpe-item":
            to_insert = CPEExtractor(cpe=self.record["cpe-23"])
            for _ in canonize(to_insert["vendor"]):
                self.insert(cpe=to_insert["cpeline"])
                self.wordcount += 1
            for _ in canonize(to_insert["product"]):
                self.insert(cpe=to_insert["cpeline"])
                self.wordcount += 1
            self.record = {}
            self.itemcount += 1
            if self.itemcount % 5000 == 0:
                time_elapsed = round(time.time() - self.start_time)
                print(
                    f"... {self.itemcount} items parsed ({self.wordcount} words) in {
                        time_elapsed} seconds"
                )

    def insert(self, cpe):
        if cpe is None:
            return False
        self.result.add(cpe)


def CPEExtractor(cpe=None):
    if cpe is None:
        return False
    record = {}
    cpefield = cpe.split(":")
    record["vendor"] = cpefield[3]
    record["product"] = cpefield[4]
    record["cpeline"] = ":".join(cpefield)
    return record


def canonize(value=None):
    value = value.lower()
    words = value.split("_")
    return words
