from importlib import import_module
import os


def auto_import():
    parents_dir = os.path.dirname(__file__).rsplit('/', 2)[-2:]
    for file in os.listdir(os.path.dirname(__file__)):
        if file[-3:] == '.py' and file not in ('__init__.py', 'default.py'):
            import_module('.'.join(parents_dir) + '.' + file.replace('.py', ''))


auto_import()
