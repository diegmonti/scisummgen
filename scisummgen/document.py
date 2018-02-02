from xml.dom import minidom


class Document:
    sentence = {}

    def __init__(self, path):
        xml = minidom.parse(path)
        tags = xml.getElementsByTagName('S')

        for s in tags:
            sid = s.attributes['sid'].value
            text = s.firstChild.nodeValue
            self.sentence[int(sid)] = text
