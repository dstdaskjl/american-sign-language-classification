import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import tensorflow as tf
from cnn import CNN
from data import Data


# HIDDEN_FUNCTIONS = ['relu', 'sigmoid', 'tanh']
# OUTPUT_FUNCTIONS = ['linear', 'sigmoid', 'softmax']
# OPTIMIZERS = ['sgd', 'rmsprop', 'adam', 'adadelta', 'adagrad']
# LOSS_FUNCTIONS = ['sparse_categorical_crossentropy']
# DROPOUT_RATES = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

HIDDEN_FUNCTIONS = ['relu', 'sigmoid', 'softmax', 'softplus', 'softsign', 'tanh', 'selu', 'elu', 'exponential']
OUTPUT_FUNCTIONS = ['relu', 'sigmoid', 'softmax', 'softplus', 'softsign', 'tanh', 'selu', 'elu', 'exponential']
OPTIMIZERS = ['sgd', 'rmsprop', 'adam', 'adadelta', 'adagrad', 'adamax', 'nadam', 'ftrl']
LOSS_FUNCTIONS = ['sparse_categorical_crossentropy']
DROPOUT_RATES = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


with tf.device('/gpu:0'):
    dataset, label = Data().load_train_dataset()
    CNN().train(dataset, label, HIDDEN_FUNCTIONS, OUTPUT_FUNCTIONS, OPTIMIZERS, LOSS_FUNCTIONS, DROPOUT_RATES)
