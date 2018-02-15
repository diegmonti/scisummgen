import unittest

import scisummgen


class SimilarityTestSuite(unittest.TestCase):

    def test_tokenize(self):
        similarity = scisummgen.Similarity
        self.assertEqual(['hello', 'world'], similarity.tokenize('Hello, World!'))
        self.assertEqual(['hello', 'world'], similarity.tokenize('Hello, This *IS* World!'))

    def test_count_tokens(self):
        similarity = scisummgen.Similarity
        self.assertEqual(0, similarity.count_tokens('Hello, World!', 'Hi!'))
        self.assertEqual(1, similarity.count_tokens('Hello, World!', 'Hello!'))
        self.assertEqual(2, similarity.count_tokens('Hello, World!', 'Hello, my world!'))

    def test_count_bigrams(self):
        similarity = scisummgen.Similarity
        self.assertEqual(0, similarity.count_bigrams('Hello, Dear World!', 'Hi Dear!'))
        self.assertEqual(1, similarity.count_bigrams('Hello, Dear World!', 'Hello Dear!'))
        self.assertEqual(2, similarity.count_bigrams('Hello, Dear World!', 'Hello, dear world Bigram!'))


if __name__ == '__main__':
    unittest.main()
