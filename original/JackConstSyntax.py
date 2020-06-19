KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var' ,'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let' ,'do', 'if', 'else', 'while', 'return']

SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|' ,'<', '>', '=', '~']

NUMHEAD = ['0','1','2','3','4','5','6','7','8','9']

C_KEYWORD = 1 #
C_CLASS = 0
C_STATIC = 5
C_FIELD = 4
C_VAR = 6
C_INT = 7
C_CHAR = 8
C_BOOLEAN = 9
C_TYPE = {7,8,9}
C_SUBROUTINE = {1,2,3}
C_CLASSVARDEC = {4,5}
C_STATEMENT = {15,16,17,19,20}
C_LET = 15
C_DO = 16
C_IF = 17
C_ELSE = 18
C_WHILE = 19
C_RETURN = 20

C_SYMBOL = 2 #
C_DOT = 6
C_COMMA = 7
C_SEMICOLON = 8
C_OP = {9,10,11,12,13,14,15,16,17}

C_IDENTIFIER = 3 #

C_INTVAL = 4 #

C_STRINGVAL = 5 #
'''
1 Keyword index(index int)
2 symbol name(index int)
3 identifier (string)
4 intVal int
5 stringVal string
'''