import unittest

import scisummgen


class PaperTestSuite(unittest.TestCase):

    def test_paper(self):
        paper = scisummgen.Paper("../scisumm-corpus/Training-Set-2017/C00-2123")
        self.assertEqual(16, len(paper.citing))
        self.assertEqual(18, len(paper.annotation.citances))

    def test_get_citance_text(self):
        paper = scisummgen.Paper("../scisumm-corpus/Training-Set-2017/C00-2123")
        citance = paper.annotation.citances[0]
        citing = paper.citing['C02-1050.xml']
        text = citing.sentence[39] + citing.sentence[40] + citing.sentence[41]
        self.assertEqual(text, paper.get_citance_text(citance))


if __name__ == '__main__':
    unittest.main()
