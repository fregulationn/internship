# -*- coding: utf-8 -*-
"""
File Name：     dev
Author :       peng.he
-------------------------------------------------
"""
import os

from sentence.settings import ModelType

MODEL_TYPE = ModelType.LR
DOMAIN_NAME = 'ie-sentence.msxf.lo'
IP = '0.0.0.0'
PORT = 9420
LOG_PATH = '/home/finance/Logs/{}/{}-{}.log'.format(DOMAIN_NAME, DOMAIN_NAME, PORT)

DATA_DIR = '/home/finance/Data/{}'.format(DOMAIN_NAME)
RAW_DATA = os.path.join(DATA_DIR, 'data.xlsx')
COUNT_VECTOR = os.path.join(DATA_DIR, 'count_vector.joblib')
LABELS = os.path.join(DATA_DIR, 'labels.joblib')
MODEL = os.path.join(DATA_DIR, 'lr_model.joblib')
