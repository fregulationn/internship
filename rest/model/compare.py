"""Performs face alignment and calculates L2 distance between the embeddings of images."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import argparse
import datetime
import re
from tensorflow.python.platform import gfile
from rest.api.data import Image


# os.environ["CUDA_VISIBLE_DEVICES"]="1"

def compare(sess_facenet, image):
    starttime = datetime.datetime.now()


    nrof_samples = 1
    img_list = [None] * nrof_samples
    for i in range(nrof_samples):
        prewhitened = prewhiten(image)
        img_list[i] = prewhitened

    images = np.stack(img_list)


    # Get input and output tensors
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

    # print(images_placeholder)
    # print(embeddings)
    # print(phase_train_placeholder)

    # Run forward pass to calculate embeddings
    print(images)
    feed_dict = {images_placeholder: images, phase_train_placeholder: False}
    emb = sess.run(embeddings, feed_dict=feed_dict)

    # print('Images:')
    # for i in range(nrof_samples):
    #     image_name =  os.path.basename(image_paths[i])
    #     print('%1d: %s' % (i, image_name))
    # print('')

    # Print distance matrix
    res_feature = emb[0,:]

    images = Image.query.all()
    min_dist = 10000
    min_pic = " "
    for image in images:
        dist = np.sqrt(np.sum(np.square(np.subtract(res_feature,Image.loads(Image,image.tmp_feature)))))
        if dist < min_dist:
            min_dist = dist
            min_pic = image.name
    
    

    
    # print('Distance matrix')

    # print('    ', end='')
    # for i in range(nrof_samples):
    #     print('    %1d     ' % i, end='')
    # print('')
    # for i in range(nrof_samples):
    #     print('%1d  ' % i, end='')
    #     for j in range(nrof_samples):
    #         dist = np.sqrt(np.sum(np.square(np.subtract(emb[i,:], emb[j, :]))))
    #         print('  %1.4f  ' % dist, end='')
    #     print('')


    endtime = datetime.datetime.now()
    print(endtime - starttime)

    return image.name



def session(model):
    tf.Graph().as_default()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    sess.as_default()
    print(sess)
    starttime1 = datetime.datetime.now()

    # Load the model
    load_model(model, sess)
    starttime2 = datetime.datetime.now()
    print("ssss%s" % (starttime2 - starttime1))
    return sess



# def parse_arguments(argv):
#     parser = argparse.ArgumentParser()
#     model_path = r"D:\Z\code\video_detect\model\20170512-110547"
#     # model_path = r"~/python/face/model"

#     parser.add_argument('img1', type=str, help='Image1input to compare')
#     parser.add_argument('img2', type=str, help='Image2 input to compare')

#     parser.add_argument('-m', '--model', type=str,
#     help = 'Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file', default = model_path)
#     parser.add_argument('--gpu_memory_fraction', type=float,
#                         help='Upper bound on the amount of GPU memory that will be used by the process.', default=0.8)

#     return parser.parse_args(argv)


def load_model(model,sess):
    # Check if the model is a model directory (containing a metagraph and a checkpoint file)
    #  or if it is a protobuf file with a frozen graph
    model_exp = os.path.expanduser(model)
    if (os.path.isfile(model_exp)):
        print('Model filename: %s' % model_exp)
        with gfile.FastGFile(model_exp, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    else:
        print('Model directory: %s' % model_exp)
        meta_file, ckpt_file = get_model_filenames(model_exp)

        print('Metagraph file: %s' % meta_file)
        print('Checkpoint file: %s' % ckpt_file)

        saver = tf.train.import_meta_graph(os.path.join(model_exp, meta_file))
        saver.restore(sess, os.path.join(model_exp, ckpt_file))

def get_model_filenames(model_dir):
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files) == 0:
        raise ValueError('No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files) > 1:
        raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
    meta_file = meta_files[0]
    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups()) >= 2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y



# if __name__ == '__main__':
#     main(parse_arguments(sys.argv[1:]))
