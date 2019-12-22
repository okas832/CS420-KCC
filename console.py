import sys
from logger import logger as Logg
from interpreter import interpreter as Interp

class Console:
    def __init__(self, filename):
        self.filename = filename
    
    def next(self):
        ## todo : execute with interpreter and update with logger
        pass
    
    def parseCommand(self, line):
        args = line.split(' ')
        if args[0] == 'next':
            if len(args) <= 1:
                self.next()
            else:
                n = int(args[1])
                for i in range(n):
                    self.next()
        elif args[0] == 'print' or args[0] == 'trace':
            if len(args) <= 1:
                print("Error: Require second arguemnt")
            else:
                Logg.command(args[0], args[1])
        elif args[0] == 'exit':
            return False
        else:
            print("Error: Invalid command")
        return True

def help():
    print("# KCC - mini-C Compiler and Interpreter ###")
    print("## Usage : python console.py <input file>")
    print("## Interpreter Commands")
    print("* next <count>")
    print("* print <varname>")
    print("* trace <varname>")

def main():
    if len(sys.argv) <= 1:
        help()
        return
    filename = sys.argv[1]
    # 1. load file and initialize console
    console = Conesole(filename)
    # 2. main loop
    while True:
        comm = input("$ ")
        loop = console.parseCommand(comm)
        if not loop:
            break
    # 3. exit

if __name__ == "__main__":
    main()