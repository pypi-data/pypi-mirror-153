from os import environ
from os.path import expanduser
from pathlib import Path
from subprocess import call


init_config = '''
config = dict(
    target = 'local',
)
'''.strip()


def get_config_all():
    path = Path('~/.config/setux').expanduser()
    try:
        from pybrary.modules import load
        full = path / 'config.py'
        config = load('config', full)
        return full, config.config
    except: pass
    try:
        from yaml import load
        full = path / 'config.yaml'
        config = load(full)
        return full, config
    except: pass
    try:
        from json import load
        full = path / 'config.json'
        config = load(full)
        return full, config
    except: pass
    return None, None


def get_config_path():
    return get_config_all()[0]


def get_config():
    return get_config_all()[1]


def edit():
    path = get_config_path()
    if not path:
        path = Path('~/.config/setux/config.py').expanduser()
        with open(path, 'w') as out:
            out.write(init_config)
    editor = environ.get('EDITOR','vim')
    call([editor, path])
