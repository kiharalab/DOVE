# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 11:49:11 2017

@author: wangxiao
"""
from __future__ import division
from keras.models import Sequential
from keras.layers import Conv3D
from keras.layers.core import Dropout, Activation,Dense,Flatten
from keras.layers.pooling import MaxPooling3D
import tensorflow as tf
from keras import backend as K
import numpy as np
import keras
import random
import os
from keras.callbacks import EarlyStopping
from keras.utils.np_utils import to_categorical
from keras.regularizers import l1,l2
from keras.constraints import maxnorm
import matplotlib.pyplot as plt
from keras.optimizers import Nadam
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import  BatchNormalization
#from keras.utils import plot_model
from keras import backend as K
import gc
import random
from ops.os_operation import mkdir
from keras.layers.advanced_activations import LeakyReLU
from ops.Extract_Indicate import Indicate_to_channel
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
#from importance_sampling.training import ImportanceTraining
from keras.callbacks import ReduceLROnPlateau
def f1score(y_true, y_pred):
    #Calculating f1score
    num_tp = K.sum(y_true*y_pred)
    num_fn = K.sum(y_true*(1.0-y_pred))
    num_fp = K.sum((1.0-y_true)*y_pred)
    num_tn = K.sum((1.0-y_true)*(1.0-y_pred))
    #print num_tp, num_fn, num_fp, num_tn
    #precision, recall


    f1 = 2.0*num_tp/(2.0*num_tp+num_fn+num_fp)
    return f1
def precision(y_true, y_pred):
    # Calculating f1score
    num_tp = K.sum(y_true * y_pred)
    num_fp = K.sum((1.0 - y_true) * y_pred)
    precison = num_tp / (num_tp + num_fp)
    return precison
def recall(y_true, y_pred):
    num_tp = K.sum(y_true * y_pred)
    num_fn = K.sum(y_true * (1.0 - y_pred))
    recall = num_tp / (num_fn + num_tp)
    return recall
def makecnn(learningrate,regular,decay,channel_number):
    #model structure
    model=Sequential()
    model.add(Conv3D(100, kernel_size=(3,3,3), strides=(1, 1, 1), input_shape = (20,20,20,channel_number),padding='valid', data_format='channels_last', dilation_rate=(1, 1, 1),  use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    #model.add(Dropout(0.3))

    model.add(Conv3D(200, kernel_size=(3,3,3), strides=(1, 1, 1), padding='valid', data_format='channels_last', dilation_rate=(1, 1, 1), use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    #model.add(Dropout(0.3))

    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=None, padding='valid', data_format='channels_last'))
    model.add(BatchNormalization(axis=1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
    model.add(Conv3D(400, kernel_size=(3,3,3),strides=(1, 1, 1), padding='valid', data_format='channels_last', dilation_rate=(1, 1, 1), use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    #model.add(Dropout(0.3))

    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=None, padding='valid', data_format='channels_last'))
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(1000, use_bias=True, input_shape = (32000,),kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.3))

    model.add(Dense(100, use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.3))

    model.add(Dense(1, activation='sigmoid', use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=l2(regular), kernel_constraint=None, bias_constraint=None))
    nadam=Nadam(lr=learningrate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=decay)
    model.compile(loss='binary_crossentropy', optimizer=nadam, metrics=['accuracy',f1score,precision,recall])
    return model