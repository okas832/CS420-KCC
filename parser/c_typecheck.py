# TODO: Traverse AST, check EXPRs type & attach appropriate type casting expressions as necessary
#       If no type cast rule exist, raise TypeError.
#       If non-pointers are DEREFed or rvalues are ADDRed, raise TypeError.
#       Assume that SVAL string literals are char[], since we don't have const.