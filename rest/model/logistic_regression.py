# -*- coding: utf-8 -*-
"""
File Name：     logistic_regression
Author :       peng.he
-------------------------------------------------
"""
from time import time
from sklearn.linear_model import LogisticRegression


def train(X_train, y_train):
    t0 = time()
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)
    return clf
