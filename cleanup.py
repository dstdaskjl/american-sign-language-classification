import sys
sys.path.append('..')

import constant as const
from pylib.path import File, Directory

file = File()
directory = Directory()

directory.delete(const.RESULT_DIR)
directory.create(const.RESULT_DIR)
directory.create(const.MODEL_DIR)
directory.create(const.HISTORY_DIR)
directory.create(const.EXCEPTION_DIR)