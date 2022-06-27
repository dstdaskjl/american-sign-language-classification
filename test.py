import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import tensorflow as tf
from cnn import CNN
from data import Data


with tf.device('/gpu:0'):
    dataset, label = Data().load_test_dataset()
    CNN().test(dataset, label)
