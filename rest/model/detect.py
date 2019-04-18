

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc

import numpy as np
import sys
import os
import argparse
import align.detect_face
import datetime
import cv2
import matplotlib.pyplot as plt
from rest import settings

# import tensorflow as tf
# from tensorflow.python.framework.graph_util import convert_variables_to_constants
# os.environ["CUDA_VISIBLE_DEVICES"]="1"

def detect_api(pnet, rnet, onet, image_path):
    starttime = datetime.datetime.now()

    img = misc.imread(os.path.expanduser(image_path), mode='RGB')
    img_size = np.asarray(img.shape)[0:2]
    
    bounding_boxes, _ = align.detect_face.detect_face(img, settings.MINIMIZE, pnet, rnet, onet, settings.threshold, settings.factor)
    nrof_faces = bounding_boxes.shape[0]  # 人脸数目

    if nrof_faces == 0:
        return

    img_list = [None] * nrof_faces
    for i in range(nrof_faces):
        face_position = np.squeeze(bounding_boxes[i, 0:4])
        det = face_position.astype(int)

        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - settings.MARGIN / 2, 0)
        bb[1] = np.maximum(det[1] - settings.MARGIN / 2, 0)
        bb[2] = np.minimum(det[2] + settings.MARGIN / 2, img_size[1])
        bb[3] = np.minimum(det[3] + settings.MARGIN / 2, img_size[0])
        cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]

        aligned = misc.imresize(cropped, (settings.IMAGE_SIZE, settings.IMAGE_SIZE), interp='bilinear')  # previous cropped
        img_list[i] = aligned
        # detect_face_output_path =args.output+"/"+str(i)+".png"
        # misc.imsave(detect_face_output_path,aligned)

        cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]), (0, 255, 0), 2)

        # plt.imshow(img)
        # plt.savefig()
        # plt.show()

    # images = np.stack(img_list)
    # print(args.output_path)

    # Output image path
    filepath,tempfilename = os.path.split(image_path)
    shotname,extension = os.path.splitext(tempfilename)
    outpath = os.path.join(filepath,shotname+"_detect"+"."+extension)

    cv2.imwrite(outpath,img)
    endtime = datetime.datetime.now()
    print(endtime - starttime)

    return img_list, outpath , bounding_boxes[0, 0:4]