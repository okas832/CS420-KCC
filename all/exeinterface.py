from ast import *
from c_yacc import AST_YACC
from c_typecheck import AST_TYPE
from interpreter import AST_INTERPRET
from ctype import *
from logger import *
from console import *

class Interface:
    def __init__(self, filename):
        self.filename = filename
        self.console = None  # set by console
        self.linecurr = -1   # previously blocked here
        self.linerem = 0     # remaining lines to exec
        self.is_running = False

    def loadfile(self):
        try:
            self.file = open(self.filename, "r").read()
        except:
            raise FileNotFoundError("Error: cannot load input file of name " + self.filename)

    def makeAST(self):
        self.AST = AST_YACC(self.file)
        self.AST = AST_TYPE(self.AST)

    def load(self):
        self.loadfile()
        self.makeAST()

    def check(self, lineno, jump=False, skip=False):
        ## currently seeing AST node @ lineno, can I execute this?
        ## compute line delta
        ## loop {
        ##  check runnable state (not runnable == linerem < 0)
        ##  if not runnable, call self.console.prompt()
        ## }
        ## return => runnable state guaranteed!

        if not self.is_running:
            return

        if not skip:
            if jump and self.linecurr != lineno:
                # executed self.linecurr, jumped to lineno
                self.linerem -= 1
            else:
                # executed [self.linecurr, lineno)
                self.linerem -= (lineno - self.linecurr)
        self.linecurr = lineno

        while self.linerem < 0:
            self.console.prompt()

    def start(self):
        try:
            AST_INTERPRET(self.AST, self)
        except Exception as e:
            print(e)
            self.is_running = False

        self.console.prompt()
