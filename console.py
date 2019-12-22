import sys
from logger import logger

class consoleErr(Exception):
    def __init__(self, _message):
        self.message = _message

class Console():
    def __init__(self, _filename):
        self.filename = _filename

    def load(self):
        # load file to interpreter and initialize logger
        pass
    
    def parseCommand(self, command):
        args = command.split(' ')
        if args[0] == 'next':
            if len(args) <= 1:
                # next(1)
                pass
            else:
                n = int(args[1])
                # next(n)
                pass
        elif args[0] == 'print':
            if len(args) <= 1:
                raise(consoleErr("Require second arg"))
            else:
                name = args[1]
                # print(name)
                pass
        elif args[0] == 'trace':
            if len(args) <= 1:
                raise(consoleErr("Require second arg"))
            else:
                name = args[1]
                # trace(name)
                pass
        elif args[0] == 'exit':
            print("Terminating...")
            return True
        else:
            raise(consoleErr("Invalid command"))
        return False

def help():
    # todo : print help message
    print("### help message here###")

def topmessage():
    # todo : print top message
    print("KCC : Mini-C Interpreter v0.0.1")
    print("CS420 Project, Fall 2019, KAIST")
    print("Main loop initiated")

def main():
    argc = len(sys.argv)
    # if no additional args, print help message
    if argc <= 1:
        help()
        return

    # 1. read filename
    filename = sys.argv[1]
    console = Console(filename)
    
    # 2. load file
    print("Loading file...")
    console.load()
    print("Load complete!")
    # 2.1. top message 
    topmessage()

    # 3. start main loop
    while True:
        try:
            command = input("$ ")
            exiting = console.parseCommand(command)
            if exiting:
                break
        except consoleErr as e:
            print("Error: " + e.message)
            

if __name__ == "__main__":
    main()