from xml.dom import minidom
from xml.parsers.expat import ExpatError


class Document:

    def __init__(self, path):
        with open(path, 'rb') as file:
            raw_content = file.read()

        content = raw_content.decode('utf-8', 'ignore')

        try:
            xml = minidom.parseString(content)
            tags = xml.getElementsByTagName('S')
            self.sentence = {}

            for s in tags:
                sid = s.attributes['sid'].value

                if sid is '':
                    continue

                text = s.firstChild.nodeValue
                self.sentence[int(sid)] = text

        except ExpatError as e:
            print('Unable to parse the file', path)
            raise e

        except ValueError as e:
            print('Unable to parse the file', path)
            raise e
