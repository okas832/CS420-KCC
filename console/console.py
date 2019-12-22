import sys

def interpLine():
    pass

def fineName():
    pass

class Console:
    def __init__(self, _filename):
        self.filename = _filename

    def next(self, count):
        for i in range(count):
            interpLine()

    def print(self, name):
        

    def trace(self, name):
        pass

    def printOut(line):
        print(line, file=sys.stdout)

    def printErr(line):
        print(line, file=sys.stderr)

    def parseCommand(self, line):
        args = line.split(' ')
        # next
        if args[0] == 'next':
            if len(args) <= 1:
                self.next(1)
            else:
                n = int(args[1])
                self.next(n)
        # print
        elif args[0] == 'print':
            if len(args) <= 1:
                printErr('Error: Need second argument for print')
            else:
                name = args[1]
                self.print(name)
        # trace
        elif args[0] == 'trace':
            if len(args) <= 1:
                printErr('Error: Need second argument for trace')
            else
                name =args[1]
                self.trace(name)
        # invalid command
        else:
            printErr('Error: Invalid command ' + args[0])