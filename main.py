import re
from os import listdir
from os.path import join

import numpy as np
from sklearn import neural_network
from sklearn.metrics import confusion_matrix

import scisummgen

training_path = 'scisumm-corpus/Training-Set-2017'
test_path = 'scisumm-corpus/Test-Set-2017'


def create_features(path):
    X = []
    y = []

    # For all the papers
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


def create_summaries(path, y_probability):
    y_index = 0

    # For all the test papers
    for directory in listdir(path):
        print('Creating summary for paper', directory)
        paper = scisummgen.Paper(join(path, directory))
        sentence_scores = np.zeros(next(iter(paper.reference.sentences.values()))['sid_max'] + 1)

        # For all the citances
        for citance in paper.annotation.citances:
            # For all the sentences of the reference paper
            for sentence_sid, sentence in paper.reference.sentences.items():
                # The probability of being a provenance
                sentence_scores[sentence_sid] += y_probability[y_index][1]
                y_index += 1

        # Find the sentences with the highest scores
        sentence_sid_sorted = sentence_scores.argsort()[::-1]
        summary_sentences = []
        tot_words = 0

        for sid in sentence_sid_sorted:
            sentence = paper.reference.sentences[sid]
            # Avoid considering the title
            if sentence['sid'] == 0:
                continue
            # Count the number of words
            words = len(re.findall('\w+', sentence['text'].lower()))
            tot_words += words
            if tot_words <= 250:
                summary_sentences.append(sentence)
            else:
                break

        # Sort sentences by sid
        summary_sentences.sort(key=lambda x: x['sid'])

        # Create the summary
        summary = ''
        for sentence in summary_sentences:
            summary += sentence['text'] + ' '
        summary = summary.strip(' ')

        with open(join('summary', directory + '.system.txt'), 'w', encoding='utf-8') as file:
            file.write(summary)


print('Creating features for the training set')
X_training, y_training = create_features(training_path)
print('Creating features for the test set')
X_test, y_test = create_features(test_path)

print('Training the classifier')
clf = neural_network.MLPClassifier(hidden_layer_sizes=(100, 100, 100, 100, 100),
                                   learning_rate_init=0.0001, verbose=True)
clf = clf.fit(X_training, y_training)
y_prediction = clf.predict(X_test)

conf_mat = confusion_matrix(y_test, y_prediction)
print('Confusion matrix on test set')
print(conf_mat)

create_summaries(test_path, clf.predict_proba(X_test))
