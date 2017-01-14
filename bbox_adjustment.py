

from __future__ import print_function
print("script launched")
import matplotlib.pyplot as plt
from PIL import Image
import site
import numpy as np
import pandas as pd
import os
import sys
import tarfile
from IPython.display import display
from IPython.display import Image as image2
from scipy import ndimage
from os.path import isfile, join
import h5py
import tensorflow as tf
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

###for preprocessing of svhn file please see svhn_prep.ipynb or *.html file###
svhn_file=h5py.File("SVHN_full.hdf5","r")
#print(svhn_file.keys())

train_dataset = svhn_file['train_dataset'][()]
#print(train_dataset.shape[0])
train_labels = svhn_file['train_labels'][()]
test_dataset = svhn_file['test_dataset'][()]
test_labels = svhn_file['test_labels'][()]
train_boxes = svhn_file['train_boxes'][()]
test_boxes = svhn_file['test_boxes'][()]
print("got all")
svhn_file.close()

svhn_file=h5py.File("SVHN_dimensions.hdf5","r")
#print(svhn_file.keys())
pic_dimensions = svhn_file['pic_dimensions'][()]
print(pic_dimensions.shape)
print("got all")
svhn_file.close()

def reshape_bbox(data):
    new_data = []
    im_resized = 32
    
    for i in range(0,pic_dimensions.shape[0]):
    #for i in range(0,10):
        width_cutaway = (pic_dimensions[i][0] - im_resized) * float(0.5)
        height_cutaway = (pic_dimensions[i][1] - im_resized) * float(0.5)
        width_resized = (float(im_resized) / pic_dimensions[i][0]) 
       # print("pic width", pic_dimensions[i][0])
        #print(width_resized)
        height_resized = float(im_resized) / pic_dimensions[i][1]
        #print("pic height", pic_dimensions[i][1])
        #print(height_resized)

        ####this is going through each digit position but we only reformat the first 4
        numlist = []
        cropped_x = data[i][0][0] * float(0.9)
        cropped_y = data[i][2][0] * float(0.8)
        #print("crop y",cropped_y)
        #print("crop x", cropped_x)
        x0_maxarr = [data[i][0][0],data[i][0][1],data[i][0][2],data[i][0][3]]
        x0_max = np.amax(x0_maxarr)
        #x0_min = np.amin(x0_maxarr)
        x0_distance = x0_max - cropped_x
        if (x0_distance == 0):
            x0_distance = 15
        #since we gave our bounding boxes some 20% cushion in previous transformation, I assume that the available digit space is 80% of 32px
        #I account for 5px digit width and thus x0 distances below 20px get enlared, x0 distances above 20 get smaller
        resize_factor = 15/float(x0_distance)
        #print(resize_factor)
        for j in range (0,4):
            digibox = [[],[],[],[]]
            #digibox[0] = round(data[i][0][j] * width_resized,1) #xo 
            digibox[0] = ((data[i][0][j] - cropped_x)*resize_factor)+2 #xo 
            digibox[1] = data[i][1][j]  * resize_factor #width
            digibox[2] = ((data[i][2][j] - cropped_y) * resize_factor)+6 #yo
            digibox[3] = data[i][3][j]  * resize_factor #height
            #print(j)
            numlist.append(digibox)
        
        #if i % 5000 == 0:
         #   print("batch done")
        new_data.append(numlist)
    print('all done')
    return new_data

train_boxes_new = reshape_bbox(train_boxes)
#test_boxes_new = reshape_bbox(test_boxes)
print(train_boxes_new[100])
print(train_boxes[100])
print(pic_dimensions[100])



mlreadyfile = h5py.File('boxes_reshaped.hdf5')
mlreadyfile['train_boxes_new'] = train_boxes_new
mlreadyfile['pic_dimensions'] = pic_dimensions
print('done deal')

