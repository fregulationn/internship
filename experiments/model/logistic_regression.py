# -*- coding: utf-8 -*-
"""
File Name：     logistic_regression
Author :       peng.he
-------------------------------------------------
"""
import os
import pickle
from time import time

from sklearn import metrics
from sklearn.linear_model import LogisticRegression


def train(out_dir, X_train, X_test, y_train, y_test, count_vectorizer):
    X_train = count_vectorizer.transform(X_train)
    X_test = count_vectorizer.transform(X_test)

    t0 = time()
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test.toarray())
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    model_path = os.path.join(out_dir, 'lr_{}.model'.format(score))
    pickle.dump(clf, open(model_path, 'wb'))

    return model_path




if __name__ == '__main__':
    train()
    # test()
    # evaluate()
