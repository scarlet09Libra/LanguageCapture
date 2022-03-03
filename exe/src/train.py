import os
import sys
import pickle
import collections
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer


languageDict = {
    0: 'ARABIC', 1: 'CZECH', 2: 'PERSIAN', 3: 'INDONESIAN', 4: 'ITALIAN', 
    5: 'DUTCH', 6: 'POLISH', 7: 'PORTUGUESE', 8: 'SPANISH', 9: 'TURKISH', 
    10: 'VIETNAMESE'
}

def getTexts():
    languages = [
        'ara.txt', 'ces.txt', 'fas.txt', 'ind.txt', 'ita.txt',
        'nld.txt', 'pol.txt', 'por.txt', 'spa.txt', 'tur.txt',
        'vie.txt'
    ]
    texts = []

    for paths in range(len(languages)):
        with open(os.path.join(os.path.dirname(__file__), '../languages/' + languages[paths])) as f:
            raw_text = f.read()
            texts.append(raw_text)
    return texts

def train(texts):
    saveTo = os.path.dirname(__file__)
    teacherLabels = languageDict

    vectorizer = TfidfVectorizer(smooth_idf = False)
    vectorizer.fit(texts)
    tfidf = vectorizer.transform(texts)
    clf = svm.SVC()
    clf.fit(tfidf, list(teacherLabels.keys()))

    with open(saveTo + '/teacher_langs.pickle', 'wb') as f:
        pickle.dump(vectorizer, f)
        pickle.dump(clf, f)

def predict(capturedTexts):
    if getattr(sys, 'frozen', False):
        loadFrom = os.path.dirname(os.path.abspath(sys.executable)).replace('dist', 'teacher_langs.pickle')
    else:
        loadFrom = os.path.dirname(__file__) + '/teacher_langs.pickle'

    with open(loadFrom, 'rb') as f:
        vectorizer = pickle.load(f)
        clf = pickle.load(f)

    capturedTfidf = vectorizer.transform(capturedTexts)
    return clf.predict(capturedTfidf).tolist()

def majority(results):
    counter = collections.Counter(results)
    return counter.most_common()[0][0]
