from ctype import *


# there are two History; global and main
class History(list):
    def __init__(self, scope, addr):
        self.add_table(scope, addr)
        self.addr_mem = addr

    # add empty HistoryTable when there is new scope
    def add_table(self, scope, addr):
        table = HistoryTable(scope, addr)
        self.append(table)

    # extremely hard case
    # break in the simple struct or sudden return of the function in the deep struct
    # executor에서 넘겨주는거 봐서 수정필요 할듯 얼마나 del 해야 하는지
    # scope : function, loop, block
    # normal execution : del once
    # continue -> del before loop (not del loop)
    # break -> del until loop (del loop)
    # return -> del until function
    def del_table(self):
        self.pop()


# One HistoryTable for the each scope (construct)
class HistoryTable:
    def __init__(self, scope, addr):
        self.scope = scope
        self.body = []
        self.addr_mem = addr

    # find variable by name in the Table
    def var_find_name(self, var):
        find = 0
        for i in range(len(self.body)):
            if self.body[i][1] == var:
                find = 1
                return i
        if not find:
            return "no"

    # find variable by address in the Table
    def var_find_addr(self, addr):
        find = 0
        for i in range(len(self.body)):
            if self.body[i][0] == addr:
                find = 1
                return i
        if not find:
            return "no"

    # add new variable to the table
    def var_declare(self, var, ctype, line, value="N/A"):
        if isinstance(ctype, TArr):
            temp = value
            if value == "N/A":
                temp = []
                for i in range(ctype.arr_size):
                    temp.append(value)
            entry = (self.addr_mem, var, [(line, tuple(temp))])
            self.addr_mem += 8
            self.body.append(entry)
        else:
            entry = (self.addr_mem, var, [(line, value)])
            self.addr_mem += 8
            self.body.append(entry)

    # add new history to the corresponding variable
    # Array인 경우 추가 수정 필요
    def var_change(self, var, ctype, line, value):
        temp = (line, value)
        index = self.var_find_name(var)

        if index == "no":
            return "no"
        else:
            self.body[index][2].append(temp)


# CLI command : print, trace
# find variable from latest scope to global scope
# if the variable is invisible, corresponding message will be printed
def command(cli, args):
    comm = cli
    t = -1

    check_arr = args.find("[")
    if check_arr != -1:
        idx = int(args[check_arr + 1])
        var = args.split("[")[0]
        check_arr = 1
    else:
        var = args

    while True:
        index = history_main[t].var_find_name(var)
        if index == "no":
            if history_main[t].scope != "function":
                t = t - 1
                continue
            else:
                index = history_global[0].var_find_name(var)
                if index == "no":
                    print("Invisible variable")
                    break
                else:
                    temp = history_global[0].body[index][2]
                    if comm == "print":
                        if check_arr == 1:
                            print(temp[-1][1][idx])
                        else:
                            print(temp[-1][1])
                    elif comm == "trace":
                        for j in range(len(temp)):
                            if check_arr == 1:
                                print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0][idx]))
                            else:
                                print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0]))
                    break
        else:
            temp = history_main[t].body[index][2]
            if comm == "print":
                if check_arr == 1:
                    print(temp[-1][1][idx])
                else:
                    print(temp[-1][1])
            elif comm == "trace":
                for j in range(len(temp)):
                    if check_arr == 1:
                        print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0][idx]))
                    else:
                        print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0]))
            break


# When there is variable declaration, add new variable to the latest HistoryTable
# require a scope : global or main (main is default)
def declare(var, ctype, line, scope="main", value="N/A"):
    if scope == "global":
        history_global[-1].var_declare(var, ctype, line, value)
    else:
        history_main[-1].var_declare(var, ctype, line, value)


# When there is change of variable value (actually assign), add new history to the variable
# automatically find its scope from bottom to the top
# there is no check for the this value is right or not (executor handle it)
def change(var, ctype, line, value):
    t = -1
    while True:
        done = history_main[t].var_change(var, ctype, line, value)
        if done == "no":
            if history_main[t].scope != "function":
                t = t - 1
                continue
            else:
                done = history_global[0].var_change(var, ctype,  line, value)
                # executor이미 error 잡아 줄것 같은데 일단 냅둠
                if done == "no":
                    print("Invisible variable")
                    break
        break


# add new HistoryTable to the main History
# require scope(function or block)
def new_scope(scope):
    addr = history_main[-1].addr_mem
    history_main.add_table(scope, addr)


# del latest HistoryTable to the main History
def end_scope():
    history_main.del_table()

addr_global = 0x7dfb14e00000
addr_main = 0x7efb14e00000

history_global = History("function", addr_global)
history_main = History("function", addr_main)