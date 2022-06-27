import sys
sys.path.append('..')

import csv
import math
import random
import json
import numpy as np
import constant as const
from PIL import Image
from pylib.path import File, Directory
from pylib.image import Image


file = File()
directory = Directory()
image = Image()

ROW_COUNT = 50
COL_COUNT = 50
CHANNEL_COUNT = 3
CATEGORIES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class Data:
    def load_train_dataset(self) -> tuple:
        dataset, label = self._load_dataset(ds_path=const.TRAIN_DIR)
        dataset = self._normalize(x=dataset)
        dataset, label = self._shuffle_inputs(x=dataset, y=label)
        return dataset, label

    def load_test_dataset(self) -> tuple:
        dataset, label = self._load_dataset(ds_path=const.TEST_DIR)
        dataset = self._normalize(x=dataset)
        dataset, label = self._shuffle_inputs(x=dataset, y=label)
        return dataset, label

    def _load_dataset(self, ds_path: str) -> tuple:
        dataset, label = list(), list()
        for cat in const.CATEGORIES:
            print(cat, 'has been loaded.')
            for filename in directory.list_dir(ds_path, cat):
                img_arr = image.to_array(src=directory.join(ds_path, cat, filename))
                dataset.append(img_arr)
            label.extend([ord(cat) - 65] * len(directory.list_dir(ds_path, cat)))
        return np.array(dataset), np.array(label)

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        return x / 255.0

    # https://github.com/keras-team/keras/issues/4298#issuecomment-258947029
    def _shuffle_inputs(self, x: np.array, y: np.array) -> tuple:
        temp = list(zip(x, y))
        random.shuffle(temp)
        x, y = zip(*temp)
        del temp
        x, y = np.array(x), np.array(y)
        return x, y
