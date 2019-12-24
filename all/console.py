from exeinterface import *
from c_yacc import *
from logger import *
from math import log10

class Console:
    def __init__(self, filename, print_code=False):
        self.filename = filename
        self.interface = Interface(filename)
        self.interface.console = self
        self.print_code = print_code
        # current line @ self.interface.linecurr

    def init(self):
        self.interface.load()

    def prompt(self):
        ifce = self.interface
        current_line = ifce.linecurr + ifce.linerem + 1
        if self.print_code:
            print('='*0x20)
            codelines = ifce.file.splitlines()
            maxl = int(log10(len(codelines))) + 1
            for line, code in enumerate(codelines):
                print('%s%s | %s' % ('!' if current_line == line + 1 else ' ', str(line + 1).zfill(maxl), code))
            print('='*0x20)
        while True:
            command = input('> ')
            args = command.split()
            if not args:
                continue
            if args[0] == 'print' or args[0] == 'trace':
                if len(args) <= 1:
                    pass
                else:
                    cli = args[0]
                    var = args[1]
                    logger.command(cli, var)
            # NEXT case
            elif args[0] == 'next':
                if not ifce.is_running:
                    print("Program already finished.")
                    continue
                cnt = 0
                if len(args) == 1:
                    cnt = 1
                else:
                    try:
                        cnt = int(args[1])
                    except ValueError:
                        cnt = 0  # force fail
                # assert more than 1 line execute
                if cnt <= 0 or len(args) > 2:
                    print("Incorrect command usage : try 'next [lines]'")
                else:
                    ifce.linerem += cnt
                    return  # maybe in runnable state
            elif args[0] == 'quit':
                exit()
            else:
                print("Unknown command '%s'" % args[0])

if __name__ == "__main__":
    console = Console("../sample_input/avg.c", print_code=True)
    console.init()
    console.interface.start()