from setux.main import banner


doc = f'''{banner}

setux [Target] [Module | Manager | Command] [*args | **kwargs]

Deploy Module, Call Manager or Execute Command on Target

Target:
    - May be passed on command line
    - Set in environement as "setux_target"
    - Set in config ( cf setux_config )
    - defaults to "local"

Module, Manager or Command:
    - Deploy Module ( see the "modules" command )
    - Call Manager ( see the "managers" command)
        ex :
            pip installed
    - Set or Get Manager's Property
        ex :
            system hostname
            system hostname:server
        shortcut:
            hostname
            hostname:server
    - Execute Command ( see the "help" command )
    - if not specified : enter REPL on Target

'''


def usage(*args):
    print(doc)
