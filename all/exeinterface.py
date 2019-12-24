from ast import *
from c_yacc import *
from interpreter import *
from ctype import *
from logger import *
from console import *

class notStatementError(Exception):
    pass

class Interface:
    def __init__(self, filename):
        self.filename = filename
        self.console = None
        self.linecurr = 0
        self.lineuntil = 0
    
    def loadfile(self):
        try:
            self.file = open(filename, "r")
        except:
            print("Error: cannot load input file of name " + filename)

    def makeAST(self):
        self.AST = AST_YACC(self.file.read())
        self.AST = AST_TYPE(self.AST)

    def load(self):
        self.loadfile()
        self.makeAST()

    def execute(AST):
        ## first, "execute" self
        ## assert given AST is STMT type
        if isinstance(AST, STMT):
            ## check start 
            # execute first stmt of that body
        else:
            raise notStatementError()
        ## check line variables before executing current node
        ## recursively execute child nodes

    def start():
        ## should execute from body of main function
        execute()
    