from pathlib import Path
from os import listdir
from importlib import import_module

path_parent = Path('./app/routes')


for module in listdir(path_parent):
    if 'router' in module:
        import_module(f'app.routes.{module[:-3]}')