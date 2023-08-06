from os import environ
from os.path import expanduser
from pathlib import Path
from subprocess import call

from setux.logger import logger
from setux.core.manage import Manager
from setux.core.package import CommonPackager


def run(target, arg):
    target(arg)

def logs(target, level=None):
    log = logger.logs(level or 'info')
    if log:
        print(open(log).read())
    else:
        print(f'    no {level} log')

def module(target, name):
    mod = target.modules.items.get(name)
    if mod:
        hlp = mod.help()
        title = f'module {name}'
        print(title)
        print('-'*len(title))
        print(hlp)
    else:
        print(f' ! unkown module ! {name}')

def modules(target, pattern=None):
    modules = target.modules.items
    print('modules')
    print('-------')
    width = len(max(modules.keys(), key=len))+4
    for name, mod in sorted(modules.items()):
        hlp = mod.help()
        first = hlp.split('\n')[0]
        if (
            not pattern
            or pattern in name
            or pattern in first.lower()
        ): print(f'{name:>{width}} {first}')

def manager(target, name):
    manager = target.managers.get(name)
    if manager:
        hlp = manager.help()
        title = f'manager {name}'
        print(title)
        print('-'*len(title))
        print(hlp)
    else:
        print(f' ! unkown manager ! {name}')

def managers(target, pattern=None):
    managers = target.managers
    print('managers')
    print('-------')
    width = len(max(managers.keys(), key=len))+4
    for name, manager in sorted(managers.items()):
        hlp = manager.help()
        first = hlp.split('\n')[0]
        if (
            not pattern
            or pattern in name
            or pattern in first.lower()
        ): print(f'{name:>{width}} {first}')

def mappings(target):
    width = 0
    packages = target.pkgmap
    if packages:
        print('packages :')
        width = len(max(packages.keys(), key=len))+4
        for name, pkg in sorted(packages.items()):
            print(f'{name:>{width}} {pkg}')

    for manager in target.managers.values():
        if isinstance(manager, CommonPackager):
            packages = manager.pkgmap
            if packages:
                print(f'{manager.manager} :')
                w = len(max(packages.keys(), key=len))+4
                width = max(width, w)
                for name, pkg in sorted(packages.items()):
                    print(f'{name:>{width}} {pkg}')

    services = target.svcmap
    if services:
        print('\nservices :')
        w = len(max(services.keys(), key=len))+4
        width = max(width, w)
        for name, svc in sorted(services.items()):
            print(f'{name:>{width}} {svc}')

def outrun(target):
    log = target.outrun
    if log:
        print(open(log).read())
    else:
        print('target outrun not defined')

def outlog(target):
    log = target.outlog
    if log:
        print(open(log).read())
    else:
        print('target outlog not defined')

def edit(target, remote):
    editor = environ.get('EDITOR','vim')
    dest = Path('/tmp/setux')
    dest.mkdir(exist_ok=True)
    path = Path(remote)
    local = f'{dest}/{path.name}'
    ok = target.fetch(remote, local, quiet=True)
    if not ok: return False
    orginal = open(local).read()
    call([editor, local])
    edited = open(local).read()
    if edited!=orginal:
        ok = target.send(local, remote)
        status = '.' if ok else 'X'
        print(f'write {remote} {status}')
        return ok
    return True

