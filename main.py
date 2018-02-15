from os import listdir
from os.path import join

from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict

import scisummgen

training_path = 'scisumm-corpus/Training-Set-2017'

X = []
y = []

# For all the training papers
for directory in listdir(training_path):
    paper = scisummgen.Paper(join(training_path, directory))
    similarity = scisummgen.Similarity(paper)

    # For all the citances
    for citance in paper.annotation.citances:
        # For all the sentences of the reference paper
        for sentence_id, sentence_text in paper.reference.sentence.items():
            citance_text = paper.get_citance_text(citance)
            # Compute the similarities between sentence_text and citance_text
            tfidf = similarity.tfidf_similarity(sentence_text, citance_text)
            lsi = similarity.lsi_similarity(sentence_text, citance_text)
            lda = similarity.lda_similarity(sentence_text, citance_text)
            bigrams = similarity.count_bigrams(sentence_text, citance_text)
            X.append([tfidf, lsi, lda, bigrams])
            # Check if this sentence is also a provenance
            if sentence_id in citance['RO']:
                y.append(1)
            else:
                y.append(-1)

clf = tree.DecisionTreeClassifier()
y_prediction = cross_val_predict(clf, X, y, cv=5)
conf_mat = confusion_matrix(y, y_prediction)
print(conf_mat)
