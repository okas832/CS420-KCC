import logger as log

print("----------------- global scope ------------------")
# global has a = "global_var : a"
log.declare("a", "TInt", 1, "global")
log.command("print", "a")

log.change("a", 3, 5)
# show global a
log.command("print", "a")

print("----------------- main scope ------------------")
# main has a, b
log.declare("a", "TInt", 2)
log.declare("d", "TInt", 2)
log.declare("b", "TInt", 2, "main", [0,0,0,0,0])
log.command("print", "b")


log.change("b", 4, [1,2,3,4,5])
log.change("b", 5, [2,4,6,8,10])
# show global a
log.command("trace", "b")

log.new_scope("function")


log.declare("a", "TInt", 2)
log.declare("d", "TInt", 2)
log.declare("b", "TInt", 2, "main", [0,0,0,0,0])
log.command("print", "b")
log.change("b", 4, [1,2,3,4,5])
log.change("b", 5, [2,4,6,8,10])
# show global a
log.command("trace", "b")