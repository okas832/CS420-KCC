from ctype import *

# there are two History; global and main
class History(list):
    def __init__(self, scope):
        self.add_table(scope)

    # add empty HistoryTable when there is new scope
    def add_table(self, scope):
        table = HistoryTable(scope)
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
    def __init__(self, scope):
        self.scope = scope
        self.body = []

    # find variable in the Table
    def var_find(self, var):
        find = 0
        for i in range(len(self.body)):
            if self.body[i][0] == var:
                find = 1
                return i
        if not find:
            return "no"

    # add new variable to the table
    def var_declare(self, var, ctype, line):
        if isinstance(ctype, TArr):
            temp = []
            for i in range(ctype.arr_size):
               temp.append("N/A")
            entry = (var, [(line, tuple(temp))])
            self.body.append(entry)
        else:
            entry = (var, [(line, "N/A")])
            self.body.append(entry)

    # add new history to the corresponding variable
    
    # Array인 경우 추가 수정 필요
    def var_change(self, var, line, value):
        change = (line, value)
        index = self.var_find(var)

        if index == "no":
            return "no"
        else:
            self.body[index][1].append(change)


# CLI command : print, trace
# find variable from latest scope to global scope
# if the variable is invisible, corresponding message will be printed
def command(cli, var):
    comm = cli
    t = -1
    while True:
        index = history_main[t].var_find(var)
        if index == "no":
            if history_main[t].scope != "function":
                t = t - 1
                continue
            else:
                index = history_global[0].var_find(var)
                if index == "no":
                    print("Invisible variable")
                    break
                else:
                    temp = history_global[0].body[index][1]
                    if comm == "print":
                        print(temp[-1][1])
                    elif comm == "trace":
                        for j in range(len(temp)):
                            print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0]))
                    break
        else:
            temp = history_main[t].body[index][1]
            if comm == "print":
                print(temp[-1][1])
            elif comm == "trace":
                for j in range(len(temp)):
                    print(var + " = " + str(temp[j][1]) + " at line " + str(temp[j][0]))
            break


# When there is variable declaration, add new variable to the latest HistoryTable
# require a scope : global or main (main is default)
def declare(var, line, scope="main"):
    if scope == "global":
        history_global[-1].var_declare(var,line)
    else:
        history_main[-1].var_declare(var,line)


# When there is change of variable value (actually assign), add new history to the variable
# automatically find its scope from bottom to the top
# there is no check for the this value is right or not (executor handle it)
def change(var, line, value):
    t = -1
    while True:
        done = history_main[t].var_change(var, line, value)
        if done == "no":
            if history_main[t].scope != "function":
                t = t - 1
                continue
            else:
                done = history_global[0].var_change(var, line, value)
                #executor이미 error 잡아 줄것 같은데 일단 냅둠
                if done == "no":
                    print("Invisible variable")
                    break
        break


# add new HistoryTable to the main History
# require scope(function or block)
def new_scope(scope):
    history_main.add_table(scope)


# del latest HistoryTable to the main History
def end_scope():
    history_main.del_table()


history_global = History("function")
history_main = History("function")

# global, main 나누지 말고 그냥 History의 0번 인덱스를 global로, 1부터를 main으로 써도 상관은 없을듯
# 각 Table 들을 포인터로 연결하는 걸 생각해서 나눴던 거였는데
# 파이썬 list가 간편해서 이용하다보니 list를 쓰면 굳이 나눌 필요가 없는 것 같음
