# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sentence_api.py
   Description :
   Author :       peng.he
   date：          2018/6/25
-------------------------------------------------
   Change Activity:
                   2018/6/25:
-------------------------------------------------
"""
import os
import re
import joblib
import logging
from flask import request
from flask import Blueprint
from rest.api import route
from rest import settings
from rest.preprocessing import split_text, NGRAM
from rest.preprocessing.get_raw_data import is_sentence, del_para_location

bp = Blueprint('rest', __name__, url_prefix='/rest')
logger = logging.getLogger('file')

if settings.MODEL_TYPE is None:
    print('model type was not specified, please check your installation!')

_model_type = settings.MODEL_TYPE

#
# def _load_model():
#     model_path = settings.MODEL
#     labels_path = settings.LABELS
#     if _model_type == settings.ModelType.LR:
#         cv_path = settings.COUNT_VECTOR
#         if os.path.isfile(model_path) and \
#                 os.path.isfile(labels_path) and \
#                 os.path.isfile(cv_path):
#             print('model files exist, load model from files')
#             model = joblib.load(model_path)
#             labels = joblib.load(labels_path)
#             c_v = joblib.load(cv_path)
#             return model, labels, c_v
#         else:
#             print('model files are incomplete!')
#             X, y, le, c_v = _get_data()
#             if X is None:
#                 return None, None, None
#             else:
#                 print('start train lr model...')
#                 from sentence.model.logistic_regression import train
#                 model = train(X, y)
#                 joblib.dump(model, model_path)
#                 return model, le, c_v
#
#
# def _get_data():
#     data_path = settings.RAW_DATA
#     if os.path.isfile(data_path):
#         from sentence.preprocessing import get_data
#         X, y, le, c_v = get_data(data_path)
#         _save_data(le, c_v)
#         return X, y, le, c_v
#     else:
#         print('raw data file={} was not found, can not train model!'.format(data_path))
#         return None, None, None, None,
#
#
# def _save_data(le, c_v):
#     joblib.dump(le, settings.LABELS)
#     joblib.dump(c_v, settings.COUNT_VECTOR)
#
#
# _model, _le, _c_v = _load_model()


@route(bp, '/predict', methods=['POST'])
def recognize_sentence():
    '''
    query:{
        'texts':[],sentences to predict
    }
    :return:
    {
        'predict':[], predict label names
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405
    texts = request.get_json()['texts']
    try:
        # if not _model and not _le and not _c_v:
        #     print('models file are incomplete, check you installation!')
        #     return None, 500
        # X = split_text(texts=texts, ngram=NGRAM)
        # X = _c_v.transform(X)
        # pred = _model.predict(X)
        result = {}
        # result['predict'] = [_le.inverse_transform(p) for p in pred]
        logger.info('SENTENCE PREDICT:request:{},predict:{}'.format(request.json, result))
        return result, 200
    except Exception as e:
        logger.error('SENTENCE ERROR:recognize_sentence request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
        return None, 500


# def _recognize_line(line):
#     if is_sentence(line):
#         m = re.search('Senten\d+(.+?)Senten\d+—.*\\\\', line)
#         if m:
#             text = m.group(1)
#             x = split_text([text], ngram=NGRAM)
#             x = _c_v.transform(x)
#             pred = _model.predict(x)[0]
#             pred = _le.inverse_transform(pred)
#             m = re.search('Senten(\d+)—.*', line)
#             if m:
#                 num_sen = m.group(1)
#                 line = line.replace('Senten' + num_sen + '—' + '？', 'Senten' + num_sen + '—' + pred)
#
#     return line


# def _recognize_file(temp_dir, file):
#     with open(file, mode='r', encoding='utf-8') as f:
#         lines = f.readlines()
#         result = [_recognize_line(line) for line in lines]
#         out_file = os.path.join(temp_dir, os.path.basename(file))
#         with open(out_file, 'w', encoding='utf-8') as f1:
#             f1.writelines(result)
#         return out_file

#
# TEMP_DIR = 'sentence'


# @route(bp, '/predict_dir', methods=['POST'])
# def recognize_files():
#     '''
#     query:{
#         'dir':'',the files under this dir will be recognized
#     }
#     :return:
#     {
#         'recognized_files':{
#             'file_path_1':'recognized_path_1',
#             'file_path_2':'recognized_path_2',
#         }
#     }
#     '''
#     if not request.is_json:
#         logger.error('Request not contains any json data.')
#         return {'error': 'Request not contains any json data.'}, 405
#
#     # 所有待识别文件存放的目录，目前支持本地目录
#     directory = request.get_json()['dir']
#     files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
#     files = [os.path.join(directory, file) for file in files]
#     try:
#         temp_dir = os.path.join(directory, TEMP_DIR)
#         os.makedirs(temp_dir, exist_ok=True)
#         recognized = {}
#         for file in files:
#             r = _recognize_file(temp_dir, file)
#             recognized[file] = r
#         logger.info('SENTENCE PREDICT:request:{},predict:{}'.format(request.json, recognized))
#         return {'recognized_files': recognized}, 200
#     except Exception as e:
#         logger.error('SENTENCE ERROR:recognize_files request:{}, error:{}'.format(request.json, e),
#                      exc_info=True)
#         return None, 500

@route(bp, '/hello', methods=['GET'])
def hello():
    print("ok")
    return {'hello':'world'}, 200


if __name__ == '__main__':

    temp_dir = r'C:\Users\peng.he\Desktop\tmp'
    file = r'C:\Users\peng.he\Desktop\吉祥人生全年综合保障计划-主条款2.txt'
    # print(_recognize_file(temp_dir, file))
