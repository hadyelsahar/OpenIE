__author__ = 'hadyelsahar'

from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from preprocessor import *

from sklearn.cross_validation import KFold

from seqlearn.perceptron import StructuredPerceptron
from seqlearn.evaluation import bio_f_score
import numpy as np

# p = Preprocessor(inputdir="../.././../../brat/data/10k-wikipedia/00")
p = Preprocessor()


kf = KFold(p.L.shape[0], n_folds=2)

for train_ids, test_ids in kf:

    L_train = p.L[train_ids]
    L_test = p.L[test_ids]
    X_train = np.zeros((0, p.X.shape[1]))
    y_train = np.zeros((0,))
    X_test = np.zeros((0, p.X.shape[1]))
    y_test = np.zeros((0,))

    for i, l in enumerate(L_train):
        start = sum(L_train[:i])
        end = sum(L_train[:i+1])
        X_train = np.vstack([X_train, p.X[start:end]])
        y_train = np.append(y_train, p.Y[start:end])

    for i, l in enumerate(L_test):
        start = sum(L_test[:i])
        end = sum(L_test[:i+1])
        X_test = np.vstack([X_test, p.X[start:end]])
        y_test = np.append(y_test, p.Y[start:end])

    clf = StructuredPerceptron()
    clf.fit(X_train, y_train, L_train)

    y_pred = clf.predict(X_test, L_test)

    print("The Bio Score for Kfold = %s" % bio_f_score(y_test, y_pred))

