import unittest

import scisummgen


class PaperTestSuite(unittest.TestCase):

    def test_init(self):
        annotation = scisummgen.Annotation("../scisumm-corpus/Training-Set-2017/C00-2123/annotation/C00-2123.ann.txt")
        self.assertEqual('C02-1050', annotation.citances[0]['CP'])
        self.assertEqual([39, 40, 41], annotation.citances[0]['CO'])
        self.assertEqual([179], annotation.citances[0]['RO'])
        self.assertEqual(18, len(annotation.citances))


if __name__ == '__main__':
    unittest.main()
