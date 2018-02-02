import unittest

import scisummgen


class DocumentTestSuite(unittest.TestCase):

    def test_xml(self):
        document = scisummgen.Document("../scisumm-corpus/Training-Set-2017/C00-2123/Reference_XML/C00-2123.xml")
        self.assertEqual("A simple extension will be used to handle this problem.", document.sentence[12])


if __name__ == '__main__':
    unittest.main()
