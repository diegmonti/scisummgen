import unittest

import scisummgen


class GensimTestSuite(unittest.TestCase):

    def test_tokenize(self):
        gensim = scisummgen.Gensim([], '../stopwords.txt')
        self.assertEqual(['hello', 'world'], gensim.tokenize('Hello, World!'))
        self.assertEqual(['hello', 'world'], gensim.tokenize('Hello, This *IS* World!'))

    def test_common_tokens(self):
        gensim = scisummgen.Gensim([], '../stopwords.txt')
        self.assertEqual(0, gensim.common_tokens('Hello, World!', 'Hi!'))
        self.assertEqual(1, gensim.common_tokens('Hello, World!', 'Hello!'))
        self.assertEqual(2, gensim.common_tokens('Hello, World!', 'Hello, my world!'))

    def test_common_bigrams(self):
        gensim = scisummgen.Gensim([], '../stopwords.txt')
        self.assertEqual(0, gensim.common_bigrams('Hello, Dear World!', 'Hi Dear!'))
        self.assertEqual(1, gensim.common_bigrams('Hello, Dear World!', 'Hello Dear!'))
        self.assertEqual(2, gensim.common_bigrams('Hello, Dear World!', 'Hello, dear world Bigram!'))


if __name__ == '__main__':
    unittest.main()