from path import Path

path = Path()

path.delete('Exception')
path.delete('Shared')
path.delete('research.py')

path.create('Exception')
path.create('Shared')

if not path.exists('Result'):
    path.create('Result')

if not path.exists('History'):
    path.create('History')
    for i in range(1, 6):
        if not path.exists('History', str(i * 1000)):
            path.create('History', str(i * 1000))

if not path.exists('Model'):
    path.create('Model')
    for i in range(1, 6):
        if not path.exists('Model', str(i * 1000)):
            path.create('Model', str(i * 1000))

path.create(path.var.used_filepath)
path.create(path.var.alive_filepath)
path.write(path.var.status_filepath, '1')

path.copy('main.py', 'research.py')