import logger as log

print("----------------- global scope ------------------")
# global has a = "global_var : a"
log.declare("a", 1, "global")
log.change("a", 3, "global_var : a")

# show global a
log.command("print", "a")

print("----------------- main scope ------------------")
# main has a, b
log.declare("a", 1)
log.declare("b", 2)

# show main a, not global a
log.command("print", "a")
log.command("print", "b")

print("----------------- change a and b ------------------")
log.change("a", 3, 4)
log.command("print", "a")
log.change("a", 4, 5)
log.command("print", "a")
log.change("a", 5, 6)
log.change("b", 4, 5)
log.change("b", 6, 10)
log.command("print", "b")
log.change("b", 8, 15)
log.command("print", "b")
log.change("b", 10, 20)

print("----------------- change end a and b ------------------")
log.command("print", "a")
log.command("print", "b")

print("----------------- trace a and b ------------------")
log.command("trace", "a")
log.command("trace", "b")

print("----------------- trace  end a and b ------------------")
print("----------------- change scope : function ------------------")
# change of scope
log.new_scope("function")
# there is no a and b on current scope, only a is exist global
log.command("print", "a")
log.command("print", "b")
log.declare("a", 19)
# now show current scope's a
log.command("print", "a")
log.change("a", 30, 40)
log.command("print", "a")

print("----------------- change scope : block ------------------")
log.new_scope("block")
# current scope is simple block, so it searches to the function scope
log.command("print", "a")
log.declare("a", 50)
log.command("print", "a")

print("----------------- scope end : block ------------------")
log.end_scope()
log.command("print", "a")
