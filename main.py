from os import listdir
from os.path import join

from sklearn import tree
from sklearn.metrics import confusion_matrix

import scisummgen

training_path = 'scisumm-corpus/Training-Set-2017'
test_path = 'scisumm-corpus/Test-Set-2017'


def create_features(path):
    X = []
    y = []

    # For all the training papers
    for directory in listdir(path):
        paper = scisummgen.Paper(join(path, directory))
        similarity = scisummgen.Similarity(paper)

        # For all the citances
        for citance in paper.annotation.citances:
            # For all the sentences of the reference paper
            for sentence_sid, sentence in paper.reference.sentences.items():
                citance_text = paper.get_citance_text(citance)

                tfidf = similarity.tfidf_similarity(sentence['text'], citance_text)
                lsi = similarity.lsi_similarity(sentence['text'], citance_text)
                bigrams = similarity.count_bigrams(sentence['text'], citance_text)

                try:
                    sid_pos = sentence['sid'] / sentence['sid_max']
                except ZeroDivisionError:
                    sid_pos = 0

                try:
                    ssid_pos = sentence['ssid'] / sentence['ssid_max']
                except ZeroDivisionError:
                    ssid_pos = 0

                try:
                    section_pos = sentence['section'] / sentence['section_max']
                except ZeroDivisionError:
                    section_pos = 0

                X.append([tfidf, lsi, bigrams, sid_pos, ssid_pos, section_pos])

                # Check if this sentence is also a provenance
                if sentence_sid in citance['RO']:
                    y.append(1)
                else:
                    y.append(-1)

    return X, y


X_training, y_training = create_features(training_path)
X_test, y_test = create_features(test_path)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_training, y_training)
y_prediction = clf.predict(X_test)
conf_mat = confusion_matrix(y_test, y_prediction)
print(conf_mat)
