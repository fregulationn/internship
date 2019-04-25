# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sentence_api.py
   Description :
   Author :       junjie.zhang
   date：          2018/6/25
-------------------------------------------------
   Change Activity:
                   2018/6/25:
-------------------------------------------------
"""
import os
import re
# import joblib
import logging
import datetime
import tensorflow as tf
import align
import collections
from flask import request

from flask import Blueprint
from rest.api import route
from rest import settings


from rest.model import face_merge
from rest.model.compare import session
from rest.model.detect import detect_api
from rest.model.compare import compare , embbeding

from rest.api.data import User,Log,Image
from rest.api.db import db


bp = Blueprint('rest', __name__, url_prefix='/rest')
logger = logging.getLogger('file')

if settings.MODEL_TYPE is None:
    print('model type was not specified, please check your installation!')

_model_type = settings.MODEL_TYPE




def _load_model():
    g1 = tf.Graph()
    g2 = tf.Graph()

    
    # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory_fraction)
    # sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    sess1 = tf.Session(config=tf.ConfigProto( log_device_placement=False),graph= g1)
    with sess1.as_default():
        with g1.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess1, None)
    
    model = settings.FACENET_MODEL
    sess_facenet = session(model , g2)
    print(sess_facenet)
    
    return pnet,rnet,onet,sess_facenet

    # model_path = settings.MODELUntitled Folder
    # labels_path = settings.LABEUntitled Folder
    # if _model_type == settings.ModelType.LR:
    #     cv_path = settings.COUNT_VECTOR
    #     if os.path.isfile(model_path) and \
    #             os.path.isfile(labels_path) and \
    #             os.path.isfile(cv_path):
    #         print('model files exist, load model from files')
    #         model = joblib.load(model_path)
    #         labels = joblib.load(labels_path)
    #         c_v = joblib.load(cv_path)
    #         return model, labels, c_v
    #     else:
    #         print('model files are incomplete!')
    #         X, y, le, c_v = _get_data()
    #         if X is None:
    #             return None, None, None
    #         else:
    #             print('start train lr model...')
    #             from sentence.model.logistic_regression import train
    #             model = train(X, y)
    #             joblib.dump(model, model_path)
    #             return model, le, c_v


pnet, rnet, onet, sess_facenet = _load_model()

def load_model_image(model_image_path):
    files = os.listdir(model_image_path)
   
    for file in files:
        if "_detect" in file:
            continue

        image = Image.query.filter(Image.imagepath == file).first()
        if image is not None:
            logger.info('LOAD_MODEL_IMAGE:skipe image_name:{}'.format(file))
            print("skip image{}".format(file))
            continue
        else:
            file_path = os.path.join(model_image_path,file)
            print("init image path : {}".format(file_path))
            face_list, _ ,_ = detect_api(pnet, rnet, onet, file_path)
            if len(face_list) > 1:
                logger.error('ERROR:load image more than one face:{}'.format(file), exc_info=True)
                
            res_feature = embbeding(sess_facenet, face_list[0])
            db.session.add(Image(imagepath = file , feature = Image.dumps(Image,res_feature)))
            db.session.commit()
            logger.info('LOAD_MODEL_IMAGE:image_name:{}'.format(file))
            
print("waiting call")

@route(bp, '/init_compare_image', methods=['GET'])
def init_compare_image():
    try:
        result = {}
        
        load_model_image(settings.MODEL_IMAGE_PATH)
        result['status'] = True
            
        logger.info('initImage:request:{},return:{}'.format(request.json, result))
        return result, 200
    except Exception as e:
        logger.error('ERROR:initImage request:{}, error:{}'.format(request.json, e), exc_info=True)
        return None, 500


@route(bp, '/checkUser' , methods = ['Post'])
def checkUser():
    '''
    query:{
        'openId', string
    }
    :return:{
        'status',boolean
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405
    username = request.get_json()['openId']
    try:
        result = {}
        user = User.query.filter(User.username == username).first()
        if user is None or user.username.strip == '':
            result['status'] = False
            db.session.add(User(username = username))
            db.session.commit()
        else:
            result['status'] = True

            
        logger.info('checkUser:request:{},return:{}'.format(request.json, result))
        return result, 200
    except Exception as e:
        logger.error('ERROR:checkUser request:{}, error:{}'.format(request.json, e), exc_info=True)
        return None, 500

@route(bp, '/user/getHistory' , methods = ['Post'])
def getHistory():
    '''
    query:{
        'openId', string
    }
    :return:{
        history
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405
    username = request.get_json()['openId']
    try:
        result = {}
        logs = Log.query.filter(Log.username == username).all()

        list_logs = []
        for log in logs:
            d = collections.OrderedDict()
            d['user_Id'] = log.username
            d['history_id'] = log.id
            d['type'] = log.type
            d['datetime'] = log.datetime
            d['outputImage'] = log.imageres
            list_logs.append(d)


        result['history'] = list_logs
        logger.info('checkUser:request:{},return:{}'.format(request.json, result))
        return result, 200
    except Exception as e:
        logger.error('ERROR:checkUser request:{}, error:{}'.format(request.json, e), exc_info=True)
        return None, 500


@route(bp, '/detect', methods=['POST'])
def detect():
    '''
    query:{
        'username': string, wechatId
        'inputImage':[], imagePath
    }
    :return:
    {
       
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405

    image_path = request.get_json()['inputImage']
    username = request.get_json()['user_Id']
    try:
        if not pnet and not onet and not rnet:
            print('models file are incomplete, check you installation!')
            return None, 500

        _, outpath,_ = detect_api(pnet, rnet, onet, image_path)

        db.session.add(Log(username = username,imageres = outpath ,datetime =datetime.datetime.now(),type = "detect" ))
        db.session.commit()

        result = {}
        result['user_Id'] = username
        result['time'] = datetime.datetime.now()
        result['type'] =  "detect"
        result['outputImage'] = outpath
        logger.info('DETECT PREDICT:request:{},predict:{}'.format(request.json, result))
        return result, 200

    except Exception as e:# def _get_data():
#     data_path = settings.RAW_DATA
#     if os.path.isfile(data_path):
#         from sentence.preprocessing import get_data
#         X, y, le, c_v = get_data(data_path)
#         _save_data(le, c_v)
#         return X, y, le, c_v
#     else:
#         print('raw data file={} was not found, can not train model!'.format(data_path))
#         return None, None, None, None,
# def _save_data(le, c_v):
#     joblib.dump(le, settings.LABELS)
#     joblib.dump(c_v, settings.COUNT_VECTOR)

        logger.error('DETECT ERROR:recognize_sentence request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
        return None, 500

@route(bp, '/recognize', methods=['POST'])
def recognize():
    '''
    query:{
        'username': string, wechatId
        'inputImage':[], imagePath
    }
    :return:
    {
        
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405

    image_path = request.get_json()['inputImage']
    username = request.get_json()['user_Id']
    try:
        if not sess_facenet:
            print('models file are incomplete, check you installation!')
            return None, 500
        
        face_list, _ ,_ = detect_api(pnet, rnet, onet, image_path)
        if len(face_list)  > 1:
            if face_list[1] is not None:
                logger.error('RECOGNIZE ERROR:more than one face request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
                return None, 500

        outpath = compare(sess_facenet, face_list[0])

        db.session.add(Log(username = username,imageres = outpath ,datetime =datetime.datetime.now(),type = "recognize" ))
        db.session.commit()

        result = {}
        result['user_Id'] = username
        result['time'] = datetime.datetime.now()
        result['type'] =  "recognize"
        result['outputImage'] = outpath
        logger.info('RECOGNIZE PREDICT:request:{},predict:{}'.format(request.json, result))
        return result, 200

    except Exception as e:
        logger.error('RECOGNIZE ERROR:recognize_sentence request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
        return None, 500


@route(bp, '/face_fusion', methods=['POST'])
def face_fusion():
    '''
    query:{
        'user_Id': string,
        'inputImage':
    }
    :return:
    {
        
    }
    '''
    if not request.is_json:
        logger.error('Request not contains any json data.')
        return {'error': 'Request not contains any json data.'}, 405

    image_path = request.get_json()['inputImage']
    username = request.get_json()['user_Id']
    try:
        if not sess_facenet:
            print('models file are incomplete, check you installation!')
            return None, 500
        
        face_list, _ ,box= detect_api(pnet, rnet, onet, image_path)
        if len(face_list) > 1:
            if face_list[1] is not None:
                logger.error('FUSION ERROR:more than one face request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
                return None, 500

        model_image = compare(sess_facenet, face_list[0])

        # Output image path
        filepath,tempfilename = os.path.split(image_path)
        shotname,extension = os.path.splitext(tempfilename)
        outpath = os.path.join(filepath,shotname+"_fusion"+extension)

        face_merge(src_img = os.path.join(settings.MODEL_IMAGE_PATH,model_image),
                dst_img= image_path,
                out_img= outpath,
                face_area= box,
                alpha=0.75,
                k_size=(15, 10),
                mat_multiple=0.95)

        db.session.add(Log(username = username,imageres = outpath ,datetime =datetime.datetime.now(),type = "fusion" ))
        db.session.commit()

        result = {}
        result['user_Id'] = username
        result['time'] = datetime.datetime.now()
        result['type'] =  "fusion"
        result['outputImage'] = outpath
        logger.info('FUSION PREDICT:request:{},predict:{}'.format(request.json, result))
        return result, 200

    except Exception as e:
        logger.error('FUSION ERROR:recognize_sentence request:{}, error:{}'.format(request.json, e),
                     exc_info=True)
        return None, 500
    

@route(bp, '/hello', methods=['GET'])
def hello():
    print("ok")
    return {'hello':'world'}, 200



if __name__ == '__main__':
    
    temp_dir = r'C:\Users\junjie.zhang\Desktop\tmp'
    file = r'C:\Users\junjie.zhang\Desktop\吉祥人生全年综合保障计划-主条款2.txt'
    # print(_recognize_file(temp_dir, file))


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
# def _save_data(le, c_v):
#     joblib.dump(le, settings.LABELS)
#     joblib.dump(c_v, settings.COUNT_VECTOR)


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
