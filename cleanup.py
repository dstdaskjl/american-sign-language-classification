import variable as var
from pylib.path import File, Directory

FILE = File()
DIR = Directory()

DIR.delete('Exception')
DIR.delete('Shared')
DIR.delete('research.py')

DIR.create('Exception')
DIR.create('Shared')

if not DIR.exists('Result'):
    DIR.create('Result')

if not DIR.exists('History'):
    DIR.create('History')
    for i in range(1, 6):
        if not DIR.exists('History', str(i * 1000)):
            DIR.create('History', str(i * 1000))

if not DIR.exists('Model'):
    DIR.create('Model')
    for i in range(1, 6):
        if not DIR.exists('Model', str(i * 1000)):
            DIR.create('Model', str(i * 1000))

DIR.create(var.USED_FILEPATH)
DIR.create(var.ALIVE_FILEPATH)
FILE.write_text(var.STATUS_FILEPATH, var.ALIVE)
