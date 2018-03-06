# Scisummgen

Scisummgen is a Python script developed as the final project for the Text Mining and Analytics course. The goal of this assignment is to create summaries of scientific publications considering the content of citing papers. The `scisumm-corpus` directory contains the corpus of papers published in the context of the [CL-SciSumm 2017](http://wing.comp.nus.edu.sg/~cl-scisumm2017/) challenge.

## Terminology

The papers that need to be summarized are called **reference papers**. Each reference paper is associated with a set of **citing papers**. The sentences of a citing paper that cite the corresponding reference paper are called **citances**. The associated sentences in the reference paper are called **provenances**. An **annotation** is a relation between a set of citances of a citing paper and a set of provenances of the corresponding reference paper.

## Process

The whole process can be executed by running the script `main.py`. The resulting summaries will be placed in the `summary` directory. Please note that the process is partially stochastic.

### Text preparation

Each reference paper is represented by a *Paper* class. This class contains the reference paper, the corresponding citing papers, and the corresponding annotations. The papers are represented by the *Document* class that contains the actual sentences. The list of annotations is represented by the *Annotation* class.

The sentences are converted to lowercase and then tokenized by means of the regular expression `\w+`. The tokens listed in the `stopwords.txt` file are ignored.

### Provenance prediction

For each reference paper, for each citance, and for each sentence of the reference paper, it is possible to compute a set of features. These features are used to train an MLP classifier with the goal of predicting if a sentence of the reference paper is a provenance or not. The features considered are the following:

* **tfidf**: the TF-IDF similarity between the two sentences as computed by `gensim`;
* **lsi**: the LSI similarity between the two sentences, as computed by `gensim` considering 50 topics;
* **bigrams**: the number of common bigrams between the two sentences;
* **sid_pos**: the position of the sentence in the reference paper;
* **ssid_pos**: the position of the sentence in the local section of the reference paper;
* **section_pos**: the position of the local section in the reference paper.

Actually, the classifier is trained to predict the probability for a sentence of being a provenance given a particular citance. These probabilities are predicted and then summed considering all the citances available for a certain reference paper.

### Ranking

## Results