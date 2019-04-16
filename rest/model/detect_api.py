

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import argparse
import align.detect_face
import datetime
import cv2
import matplotlib.pyplot as plt


from tensorflow.python.framework.graph_util import convert_variables_to_constants


os.environ["CUDA_VISIBLE_DEVICES"]="1"

def main(args):
    starttime = datetime.datetime.now()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    print(args.output)
    print(args.input)

    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    print('Creating networks and loading parameters')
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)

            # pb_file_path = "D:/Z/model/"
            # # sess.run(tf.global_variables_initializer())
            # path = os.path.dirname(os.path.abspath(pb_file_path))
            # if os.path.isdir(path) is False:
            #     os.makedirs(path)
            #
            # temp = ['pnet/conv4-2/BiasAdd', 'pnet/prob1', 'rnet/conv5-2/conv5-2',
            #         'rnet/prob1', 'onet/conv6-2/conv6-2', 'onet/conv6-3/conv6-3', 'onet/prob1']
            # print(sess.graph_def)
            #
            # # convert_variables_to_constants 需要指定output_node_names，list()，可以多个
            # minimal_graph = convert_variables_to_constants(sess, sess.graph_def, temp)
            # tf.train.write_graph(minimal_graph, pb_file_path, 'mtcnn_graph.pb', as_text=False)


    img = misc.imread(os.path.expanduser(args.input), mode='RGB')
    img_size = np.asarray(img.shape)[0:2]

    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]  # 人脸数目

    if nrof_faces == 0:
        return

    img_list = [None] * nrof_faces
    for i in range(nrof_faces):
        face_position = np.squeeze(bounding_boxes[i, 0:4])
        det = face_position.astype(int)

        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - args.margin / 2, 0)
        bb[1] = np.maximum(det[1] - args.margin / 2, 0)
        bb[2] = np.minimum(det[2] + args.margin / 2, img_size[1])
        bb[3] = np.minimum(det[3] + args.margin / 2, img_size[0])
        cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]

        aligned = misc.imresize(cropped, (args.image_size, args.image_size), interp='bilinear')  # previous cropped
        detect_face_output_path =args.output+"/"+str(i)+".png"
        misc.imsave(detect_face_output_path,aligned)

        cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]), (0, 255, 0), 2)


        plt.imshow(img)
        plt.show()



    # images = np.stack(img_list)
    # print(args.output_path)
    endtime = datetime.datetime.now()
    print(endtime - starttime)




def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    model_path = r"D:\Z\code\video_detect\model\20170512-110547"

    # model_path = r"~/python/face/model"

    parser.add_argument('input', type=str, help='Images input')
    parser.add_argument('output', type=str, help='Images output floder')

    parser.add_argument('-m', '--model', type=str,
    help = 'Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file', default = model_path)
    parser.add_argument('--image_size', type=int,
    help = 'Image size (height, width) in pixels.', default = 160)
    parser.add_argument('--margin', type=int,
    help = 'Margin for the crop around the bounding box (height, width) in pixels.', default = 4)
    parser.add_argument('--gpu_memory_fraction', type=float,
    help = 'Upper bound on the amount of GPU memory that will be used by the process.', default = 0.08)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
