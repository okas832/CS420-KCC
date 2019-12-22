from sys import *

# pseudo-class for interpreter interface
# must be implemented with interpreter.py
class interface():
    def __init__(self, _filename):
        self.filename = _filename
        self.lineCount = 0
        self.lineNum = 0
        self.loaded = False

    def loadfile(self):
        self.loaded = True
        self.file = open(filename, 'r')
        ## todo : set lineCount and lineNum

    def interp(self, num):
        ## interprete until line of given number
        pass

    def next(self):
        if self.lineNum > self.lineCount:
            print("Error: file reached end", file=stderr)
            return False
        else:
            self.interp(self.lineNum)
            self.lineNum += 1
            return True

    def currentValue(self, name):
        ## find variable of name and return
        pass

    def command(self, arg):
        args = arg.split(' ')
        # case : next
        if args[0] == 'next':
            if len(args) <= 1:
                self.next()
            else:
                n = int(args[1])
                for i in range(n):
                    result = self.next()
                    if not result:
                        break
                    # todo : break if end or error
        # case : print
        elif args[0] == 'print':
            if len(args) <= 1:
                print("Error: provide second argument", file=stderr)
            else:
                name = args[1]
                value = self.currentValue(name)
                print(value)
        elif args[0] == 'trace':
            if len(args) <= 1:
                print("Error: provide second argument", file=stderr)
            else:
                name = args[1]
                # todo : print trace of var of given name
                # ? how trace information should be stored?
        else:
            print("Error: invalid command", file=stderr)
