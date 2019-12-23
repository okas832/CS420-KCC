from interpreter import *

def getlineno(AST):
    try:
        return AST.lineno
    catch Exception:
        print("Error: that AST has no lineno")
        return None