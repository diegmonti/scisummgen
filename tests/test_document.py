import unittest

import scisummgen


class DocumentTestSuite(unittest.TestCase):

    def test_init(self):
        document = scisummgen.Document("../scisumm-corpus/Training-Set-2017/C00-2123/Reference_XML/C00-2123.xml")
        self.assertEqual(12, document.sentences[12]['sid'])
        self.assertEqual(203, document.sentences[12]['sid_max'])
        self.assertEqual(12, document.sentences[12]['ssid'])
        self.assertEqual(16, document.sentences[12]['ssid_max'])
        self.assertEqual(1, document.sentences[12]['section'])
        self.assertEqual(5, document.sentences[12]['section_max'])
        self.assertEqual("A simple extension will be used to handle this problem.", document.sentences[12]['text'])


if __name__ == '__main__':
    unittest.main()
