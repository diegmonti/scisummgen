import unittest

import scisummgen


class PaperTestSuite(unittest.TestCase):

    def test_paper(self):
        paper = scisummgen.Paper("../scisumm-corpus/Training-Set-2017/C00-2123")
        self.assertEqual(16, len(paper.citing))
        self.assertEqual(18, len(paper.annotation.citances))


if __name__ == '__main__':
    unittest.main()
