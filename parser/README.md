# KCC Parser

## TODO
- [x] Define nodes for AST
- [x] Implement yacc for function body
- [x] Add line number to every AST nodes
- [x] Fix if-then vs. if-then-else shift/reduce conflict (PLY currently resolves to shift, which is correct)
- [x] Implement implicit type conversion
- [x] Implement simple type checks
- [x] Check if conditionals expression must be casted to TInt => should be done by interpreter
- [x] Add JUMP statement for yacc (continue, break, return)
- [x] Check return type of function
- [x] Add typing rule for PREOP and POSTOP

## Grammar
```
translation_unit
	: external_declaration
	| translation_unit external_declaration
	;

external_declaration
	: function_definition
	| declaration
	;

statement_list
	: statement
	| statement_list statement
	;

statement
	: compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	;

compound_statement
	: '{' '}'
	| '{' statement_list '}'
	| '{' declaration_list '}'
	| '{' declaration_list statement_list '}'
	;

declaration_list
	: declaration
	| declaration_list declaration
	;

declaration
	: type_specifier declarator_list ';'
	;

type_specifier
	: VOID
	| CHAR
	| INT
	| FLOAT
	| DOUBLE
	;

declarator_list
	: declarator
	| declarator_list ',' declarator
	;

declarator
	: pointer direct_declarator
	| direct_declarator
	;

pointer
	: '*'
	| '*' pointer
	;

direct_declarator
	: IDENTIFIER
	| IDENTIFIER '[' CONSTANT ']'
	;

expression_statement
	: ';'
	| expressions ';'
	;

expressions
	: expression
	| expressions ',' expression
	;

expression
	: logical_or_expression
	| postfix_expression assignment_operator expression
	| '*' unary_expression assignment_operator expression
	;

assignment_operator
	: '='
	| MUL_ASSIGN
	| DIV_ASSIGN
	| MOD_ASSIGN
	| ADD_ASSIGN
	| SUB_ASSIGN
	| LEFT_ASSIGN
	| RIGHT_ASSIGN
	| AND_ASSIGN
	| XOR_ASSIGN
	| OR_ASSIGN
	;

logical_or_expression
	: logical_and_expression
	| logical_or_expression OR_OP logical_and_expression
	;

logical_and_expression
	: inclusive_or_expression
	| logical_and_expression AND_OP inclusive_or_expression
	;

inclusive_or_expression
	: exclusive_or_expression
	| inclusive_or_expression '|' exclusive_or_expression
	;

exclusive_or_expression
	: and_expression
	| exclusive_or_expression '^' and_expression
	;

and_expression
	: equality_expression
	| and_expression '&' equality_expression
	;

equality_expression
	: relational_expression
	| equality_expression EQ_OP relational_expression
	| equality_expression NE_OP relational_expression
	;

relational_expression
	: shift_expression
	| relational_expression '<' shift_expression
	| relational_expression '>' shift_expression
	| relational_expression LE_OP shift_expression
	| relational_expression GE_OP shift_expression
	;

shift_expression
	: additive_expression
	| shift_expression LEFT_OP additive_expression:
	| shift_expression RIGHT_OP additive_expression
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' multiplicative_expression
	| additive_expression '-' multiplicative_expression
	;

multiplicative_expression
	: unary_expression
	| multiplicative_expression '*' unary_expression
	| multiplicative_expression '/' unary_expression
	| multiplicative_expression '%' unary_expression
	;

unary_expression
	: postfix_expression
	| INC_OP unary_expression
	| DEC_OP unary_expression
	| unary_operator unary_expression
	;

unary_operator
	: '&'
	| '*'
	| '+'
	| '-'
	| '~'
	| '!'
	;

postfix_expression
	: primary_expression
	| postfix_expression '[' expressions ']'
	| postfix_expression '(' ')'
	| postfix_expression '(' argument_expression_list ')'
	| postfix_expression INC_OP
	| postfix_expression DEC_OP
	;

argument_expression_list
	: expression
	| argument_expression_list ',' expression
	;

primary_expression
	: IDENTIFIER
	| CONSTANT
	| STRING_LITERAL
	| '(' expressions ')'
	;

selection_statement
	: IF '(' expressions ')' statement
	| IF '(' expressions ')' statement ELSE statement
	;

iteration_statement
	: WHILE '(' expressions ')' statement
	| DO statement WHILE '(' expressions ')' ';'
	| FOR '(' expression_statement expression_statement ')' statement
	| FOR '(' expression_statement expression_statement expressions ')' statement
	;

jump_statement
	| CONTINUE ';'
	| BREAK ';'
	| RETURN ';'
	| RETURN expressions ';'
	;

function_definition
	: type_specifier function_declarator compound_statement
	;

function_declarator
	: direct_declarator '(' parameter_list ')'
	| direct_declarator '(' VOID ')'
	| direct_declarator '(' ')'
	;

parameter_list
	: parameter_declaration
	| parameter_list ',' parameter_declaration
	;

parameter_declaration
	: type_specifier declarator
	;

translation_unit = goal
external_declaration = def
```
