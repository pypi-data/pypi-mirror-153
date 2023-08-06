docs = dict(
    run = '''run shell cmd on target
    ''',
    module = '''show module's help
    ''',
    modules = '''list modules
        arg = search pattern
    ''',
    manager = '''show manager's help
    ''',
    managers = '''list managers
        arg = search pattern
    ''',
    mappings = '''list mappings
    ''',
    logs = '''show log file
        arg = level (default to "info")
    ''',
    outrun = '''show commands history
    ''',
    outlog = '''show commands log
    ''',
    edit = '''edit remote file
        arg = file path to edit
    '''
)

def help(cmd=None):
    def title(txt):
        print(txt)
        print('-'*len(txt))

    if cmd:
        hlp = docs.get(cmd)
        if hlp:
            title(cmd)
            print(hlp)
        else:
            print(f'unkown command "{cmd}"')
    else:
        title('commands')
        width = len(max(docs.keys(), key=len))+4
        for cmd, hlp in sorted(docs.items()):
            first = hlp.split('\n')[0]
            print(f'{cmd:>{width}} {first}')


