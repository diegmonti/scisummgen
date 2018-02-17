import os
import re

from gensim import corpora, models, matutils

from .paper import Paper

if os.path.exists('stopwords.txt'):
    stopwords_path = 'stopwords.txt'
else:
    stopwords_path = '../stopwords.txt'

stopwords = []

with open(stopwords_path, encoding='utf-8') as f:
    for line in f.readlines():
        stopwords.append(line.strip())

stopwords = set(stopwords)


class Similarity:

    def __init__(self, list_or_paper):
        if isinstance(list_or_paper, Paper):
            paper = list_or_paper
            sentences = list(paper.reference.sentences.values())
            for citing in paper.citing.values():
                for sentence in citing.sentences.values():
                    sentences.append(sentence)
        else:
            sentences = list_or_paper

        documents = []
        for sentence in sentences:
            documents.append(self.tokenize(sentence['text']))

        self.dictionary = corpora.Dictionary(documents)
        corpus = [self.dictionary.doc2bow(document) for document in documents]
        self.tfidf = models.TfidfModel(corpus)
        self.corpus_tfidf = self.tfidf[corpus]
        self.lsi = None
        self.lda = None

    def tfidf_similarity(self, s1, s2):
        t1 = self.tokenize(s1)
        v1 = self.dictionary.doc2bow(t1)
        v1_tfidf = self.tfidf[v1]

        t2 = self.tokenize(s2)
        v2 = self.dictionary.doc2bow(t2)
        v2_tfidf = self.tfidf[v2]

        return matutils.cossim(v1_tfidf, v2_tfidf)

    def lsi_similarity(self, s1, s2):
        if self.lsi is None:
            self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=50)

        t1 = self.tokenize(s1)
        v1 = self.dictionary.doc2bow(t1)
        v1_lsi = self.lsi[v1]

        t2 = self.tokenize(s2)
        v2 = self.dictionary.doc2bow(t2)
        v2_lsi = self.lsi[v2]

        return matutils.cossim(v1_lsi, v2_lsi)

    def lda_similarity(self, s1, s2):
        if self.lda is None:
            self.lda = models.LdaModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=50)

        t1 = self.tokenize(s1)
        v1 = self.dictionary.doc2bow(t1)
        v1_lda = self.lda[v1]

        t2 = self.tokenize(s2)
        v2 = self.dictionary.doc2bow(t2)
        v2_lda = self.lda[v2]

        return matutils.cossim(v1_lda, v2_lda)

    @staticmethod
    def count_tokens(s1, s2):
        t1 = Similarity.tokenize(s1)
        t2 = Similarity.tokenize(s2)

        return len(list(set(t1).intersection(t2)))

    @staticmethod
    def count_bigrams(s1, s2):
        t1 = Similarity.tokenize(s1)
        t2 = Similarity.tokenize(s2)

        def create_bigrams(tokens):
            bigrams = []
            last_token = None
            for token in tokens:
                if last_token is not None:
                    bigrams.append(last_token + '_' + token)
                last_token = token
            return bigrams

        b1 = create_bigrams(t1)
        b2 = create_bigrams(t2)

        return len(list(set(b1).intersection(b2)))

    @staticmethod
    def tokenize(string):
        raw_tokens = re.findall('\w+', string.lower())
        tokens = []
        for token in raw_tokens:
            if token not in stopwords:
                tokens.append(token)
        return tokens
