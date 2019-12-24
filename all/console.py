from exeinterface import *
from c_yacc import *
from logger import *

class fileError(Exception):
    pass
class commandError(Exception):
    pass

class Console:
    def __init__(self, filename):
        self.filename = filename
        self.interface = Interface(filename)
        self.interface.console = self
        self.linecurr = 0

    def init(self):
        self.interface.load()

    def prompt(self, interpcurline):
        self.linecurr = interpcurline
        while True:
            command = input('> ')
            args = command.split(' ')
            if args[0] == 'print' or args[0] == 'trace':
                if len(args) <= 1:
                    raise commandError()
                else:
                    cli = args[0]
                    var = args[1]
                    logger.command(cli, var)
            elif args[0] == 'next':
                cnt = 0
                if len(args) <= 1:
                    cnt = 1
                else:
                    cnt = int(args[1])
                self.interface.lineuntil = self.linecurr + cnt
                return

def main():
    console = console("input.c")
    console.init()
    console.interface.start()