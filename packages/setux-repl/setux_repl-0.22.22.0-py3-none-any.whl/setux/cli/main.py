from os import environ
from os.path import expanduser
from sys import argv
from types import GeneratorType

from pybrary.command import Command, Param, ValidationError
from pybrary.net import ParamIPv4
from pybrary.ssh import ParamSSH

from setux.core.package import CommonPackager
from setux.targets import Local, SSH
from setux.logger import debug
from setux.commands import commands
from setux.cli.config import get_config
from setux.repl.repl import repl
from .usage import usage


class TargetParam(Param):
    '''Target
    SSH or Local Host
    '''
    name = 'target'
    positional = True
    mandatory = True
    default = 'local'

    def verify(self, value):
        outdir = self.get('outdir') or expanduser('~/setux')

        if value=='local':
            return Local(outdir=outdir)

        try:
            host = ParamSSH(self).validate(value)
        except ValidationError:
            raise ValidationError(f'{value} is not a valid target')

        target = SSH(
            name   = self.name,
            host   = value,
            outdir = outdir,
        )

        if not target or not target.cnx:
            raise ValidationError(f'{value} is unreachable')

        return target


class CommandParam(Param):
    '''Command
    Setux Command
    '''
    name = 'command'
    positional = True

    def verify(self, value):
        command = commands.get(value)
        if command:
            return command
        raise ValidationError(f'Command {value} not found')


class CommandCmd(Command):
    '''command
    Execute command
    '''
    vargs = True

    def run(self):
        target = self.get('target')
        command = self.get('command')
        if not command:
            raise ValidationError('no command')
        command(target, *self.args, **self.kws)


class ModuleParam(Param):
    '''Module
    Setux Module
    '''
    name = 'module'
    positional = True

    def verify(self, value):
        target = self.get('target')
        if value in target.modules.items:
            return value
        raise ValidationError(f'Module {value} not found')


class DeployCmd(Command):
    '''deploy
    Deploy Module
    '''
    vargs = True

    def run(self):
        target = self.get('target')
        name = self.get('module')
        if self.args:
            commands['module'](target, name)
            m = "module's arguments must be keyword arguments\n"
            print(f'\n ! invalid argument : {" ".join(self.args)} !\n ! {m}')
            return

        k = {k:v for k,v in self.kws.items() if not k.startswith('_')}
        if name=='infos': k['report'] = 'quiet'
        try:
            target.deploy(name, **k)
        except KeyError as x:
            commands['module'](target, name)
            key = x.args[0]
            print(f'\n ! missing argument : {key}  !\n')


class ManagerParam(Param):
    '''Manager
    Setux Manager
    '''
    name = 'manager'
    positional = True

    def verify(self, value):
        target = self.get('target')
        if value in target.managers:
            return value
        raise ValidationError(f'Manager {value} not found')


class ActionParam(Param):
    '''Action
    Manager Action
    '''
    name = 'action'
    positional = True

    def verify(self, value):
        return value


class ManageCmd(Command):
    '''manage
    Manager command
    '''
    vargs = True

    def run(self):
        target = self.get('target')
        name = self.get('manager')
        action = self.get('action')
        manager = getattr(target, name)

        if ':' in action:
            attr, _, val = action.partition(':')
            setattr(manager, attr, val)
        else:
            action = getattr(manager, action)
            if callable(action):
                result = action(*self.args)
                if isinstance(result, GeneratorType):
                    for vals in result:
                        print('\t'.join(vals))
                else:
                    print(result)
            else:
                print(action)


class MethodParam(Param):
    '''Method
    Target or Manager method or attribute
    '''
    name = 'method'
    positional = True

    def verify(self, value):
        target = self.get('target')

        if hasattr(target, value):
            method = getattr(target, value)
            return method

        if ':' in value:
            meth, _, val = value.partition(':')
        else:
            meth = value

        for manager in target.managers.values():
            if isinstance(manager, CommonPackager): continue
            if hasattr(manager, meth):
                method = getattr(manager, meth)
                if callable(method):
                    return method
                else:
                    self.set('manager', manager)
                    return value

        raise ValidationError(f'Invalid method "{value}" for target "{target}"')


class MethodCmd(Command):
    '''method
    Execute target method
    or get/set target attribute
    '''
    vargs = True

    def run(self):
        target = self.get('target')
        method = self.get('method')
        if callable(method):
            result = method(*self.args, **self.kws)
            if isinstance(result, GeneratorType):
                for vals in result:
                    print('\t'.join(map(str, vals)))
            else:
                print(result)
        else:
            manager = self.get('manager')
            name = '.'.join(str(manager).split('.')[1:])
            if ':' in method:
                attr, _, val = method.partition(':')
                val1 = getattr(manager, attr)
                setattr(manager, attr, val)
                val2 = getattr(manager, attr)
                if val2 != val1:
                    print(f'    {name}.{attr}:{val1} -> {val2}')
            else:
                value = getattr(manager, method)
                print(f'    {name}.{method} == {value}')


class MainCmd(Command):
    '''setux
    Setux commands
    '''
    subs = dict(
        command = CommandCmd(
            CommandParam,
        ),
        deploy = DeployCmd(
            ModuleParam,
        ),
        manage = ManageCmd(
            ManagerParam,
            ActionParam,
        ),
        method = MethodCmd(
            MethodParam,
        ),
    )


class ReplCmd(Command):
    '''REPL
    Setux REPL
    '''
    def run(self):
        target = self.get('target')
        cmd = MainCmd()
        cmd.parent = self.parent
        repl(target, cmd)


class CliCmd(Command):
    '''cli
    Setux cli
    '''
    config = get_config()
    subs = dict(
        repl = ReplCmd(),
        **MainCmd.subs,
        help = usage,
    )


def main():
    cli = CliCmd(
        TargetParam,
    )
    cli()

