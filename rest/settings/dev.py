# -*- coding: utf-8 -*-
"""
File Name：     dev
Author :       junjie.zhang
-------------------------------------------------
"""
import os

from rest.settings import ModelType

MODEL_TYPE = ModelType.LR

DOMAIN_NAME = 'rest.python.lo'
IP = '0.0.0.0'
PORT = 9420

# LOG_PATH = '/home/finance/Logs/{}/{}-{}.log'.format(DOMAIN_NAME, DOMAIN_NAME, PORT)
#

# DATA_DIR = '/home/finance/Data/{}'.format(DOMAIN_NAME)
# RAW_DATA = os.path.join(DATA_DIR, 'data.xlsx')
# COUNT_VECTOR = os.path.join(DATA_DIR, 'count_vector.joblib')
# LABELS = os.path.join(DATA_DIR, 'labels.joblib')
# MODEL = os.path.join(DATA_DIR, 'lr_model.joblib')

LOG_PATH = './Logs/{}/{}-{}.log'.format(DOMAIN_NAME, DOMAIN_NAME, PORT)

#Detect
MINIMIZE = 20  # minimum size of face
DETECT_THRESHOLD = [0.6, 0.7, 0.7]  # three steps's threshold
FACTOR = 0.709  # scale factor
MARGIN = 4 #Margin for the crop around the bounding box (height, width) in pixels.
IMAGE_SIZE = 160 #Image size (height, width) in pixels.
FACENET_MODEL = "facenet/data/20180408-102900" #Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file

MODEL_IMAGE_PATH = "/home/junjie/Code/python_REST/images/model_pic"