from ast import *
from c_yacc import *
from interpreter import *
from ctype import *
from logger import *
from console import *

class Interface:
    def __init__(self, filename):
        self.filename = filename
        self.console = None
        self.linenum = 0
        self.linecnt = 0
    
    def loadfile(self):
        try:
            self.file = open(filename, "r")
        except:
            print("Error: cannot load input file of name " + filename)

    def makeAST(self):
        self.AST = AST_YACC(self.file.read())
        self.AST = AST_TYPE(self.AST)

    def init(self):
        self.loadfile()
        self.makeAST()

    def executelin():
        # todo : execute just one line by AST lineno info and linenum
        # then update linecnt
        pass

    def execute(self):
        if self.linecnt == 0:
            self.console.prompt()
        self.executeline()
        execute()
        

    def start():
        execute()
    