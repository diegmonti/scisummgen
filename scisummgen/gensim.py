import re

from gensim import corpora, models, matutils


class Gensim:

    def __init__(self, documents, stopwords_path):
        self.stopwords = []
        with open(stopwords_path, encoding='utf-8') as f:
            for line in f.readlines():
                self.stopwords.append(line.strip())
        self.stopwords = set(self.stopwords)

        texts = []
        for document in documents:
            texts.append(self.tokenize(document))
        self.dictionary = corpora.Dictionary(texts)
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.tfidf = models.TfidfModel(corpus)
        corpus_tfidf = self.tfidf[corpus]
        self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=100)

    def tfidf_similarity(self, s1, s2):
        t1 = self.tokenize(s1)
        v1 = self.dictionary.doc2bow(t1)
        v1_tfidf = self.tfidf[v1]

        t2 = self.tokenize(s2)
        v2 = self.dictionary.doc2bow(t2)
        v2_tfidf = self.tfidf[v2]

        return matutils.cossim(v1_tfidf, v2_tfidf)

    def lsi_similarity(self, s1, s2):
        t1 = self.tokenize(s1)
        v1 = self.dictionary.doc2bow(t1)
        v1_lsi = self.lsi[v1]

        t2 = self.tokenize(s2)
        v2 = self.dictionary.doc2bow(t2)
        v2_lsi = self.lsi[v2]

        return matutils.cossim(v1_lsi, v2_lsi)

    def common_tokens(self, s1, s2):
        t1 = self.tokenize(s1)
        t2 = self.tokenize(s2)

        return len(list(set(t1).intersection(t2)))

    def common_bigrams(self, s1, s2):
        pass

    def tokenize(self, string):
        raw_tokens = re.findall('\w+', string.lower())
        tokens = []
        for token in raw_tokens:
            if token not in self.stopwords:
                tokens.append(token)
        return tokens
