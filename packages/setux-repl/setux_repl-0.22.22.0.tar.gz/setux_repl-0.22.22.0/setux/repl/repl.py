import readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

from cmd import Cmd

from setux.main import banner
from setux.commands import commands, help


def safe(cmd, target):
    def wrapper(*a, **k):
        # cmd.onecommand set an empty arg
        a = [i for i in a if not isinstance(i, str) or i.strip()]
        try:
            cmd(target, *a, **k)
        except Exception as x:
            print(type(x).__name__, x)
    return wrapper


class Repl(Cmd):
    def __init__(self, target, command):
        self.command = command
        user = target.login.name
        host = target.system.hostname
        self.prompt = f'{user}@{host} > '
        for name, cmd in commands.items():
            setattr(self, f'do_{name}', safe(cmd, target))
        super().__init__()

    def do_help(self, cmd):
        help(cmd)

    def preloop(self):
        print(banner)
        self.onecmd('infos')

    def default(self, line):
        self.command(line)

    def do_EOF(self, arg):
        return True


def repl(target, cmd):
    Repl(target, cmd).cmdloop()
