from ctype import *
from environ import *


# there are two History; global and main
class History(list):
    def __init__(self, scope):
        self.add_table(scope)

    # add empty HistoryTable when there is new scope
    def add_table(self, scope):
        table = HistoryTable(scope)
        self.append(table)

    # scope : function, loop, block
    # normal execution : del once
    # continue -> del before loop (not del loop)
    # break -> del until loop (del loop)
    # return -> del until function
    # DONE by interpreter
    def del_table(self):
        self.pop()


# One HistoryTable for the each scope (construct)
class HistoryTable:
    def __init__(self, scope):
        self.scope = scope
        self.body = {}

    # find variable by name in the Table
    def var_find_name(self, name):
        if name in self.body:
            return self.body[name]
        return None

    # add new variable to the table
    def var_declare(self, name, var):
        self.body[name] = var

    """
    # add new history to the corresponding variable
    def var_change(self, var, line, value):
        entry = self.var_find_name(var)

        if index is None:
            return False
        arr = entry[-1][1][idx]
            arr[idx] = value
            temp = (line, arr)
        else:
            temp = (line, value)
        self.body[index][2].append(temp)
        return True
    """


# CLI command : print, trace
# find variable from latest scope to global scope
# if the variable is invisible, corresponding message will be printed
def command(comm, args):
    for t in reversed(range(len(history_main))):
        var = history_main[t].var_find_name(args)
        if var is None and history_main[t].scope != "function":
            continue
        elif var is None and history_main[t].scope == "function":
            var = history_global[0].var_find_name(var)
            if var is None:
                print("Invisible variable")
                return
        if comm == "print":
            print(var)
            return
        elif comm == "trace":
            for lineno, value in var.history:
                print("%s = %s at line %d" % (var.name, value if value is not None else "N/A", lineno))
            return
    print("Invisible variable")
    return


# When there is variable declaration, add new variable to the latest HistoryTable
# require a scope : global or main (main is default)
def declare(name, var, scope="main"):
    if scope == "global":
        history_global[-1].var_declare(name, var)
    else:
        history_main[-1].var_declare(name, var)


"""
# When there is change of variable value (actually assign), add new history to the variable
# automatically find its scope from bottom to the top
# there is no check for the this value is right or not (executor handle it)
def change(var, line, value):
    for t in reversed(range(len(history_main))):
        done = history_main[t].var_change(var, line, value)
        if done is False and history_main[t].scope != "function":
            pass
        elif done is False and history_main[t].scope == "function":
            done = history_global[0].var_change(var, line, value)
            if done is False:
                print("Invisible variable")
                return
"""


# add new HistoryTable to the main History
# require scope(function or block)
def new_scope(scope):
    history_main.add_table(scope)


# del latest HistoryTable to the main History
def end_scope():
    history_main.del_table()


# start address of memory
# they are just chosen for showing some static value (far from real world)

history_global = History("function")
history_main = History("function")
