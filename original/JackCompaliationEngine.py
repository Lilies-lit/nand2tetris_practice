from JackConstSyntax import *

def compileClass():
    pass

def compileClassVarDec():
    pass

def compileSubroutine():
    pass

def compileParameterList():
    pass

def compileVarDec():
    pass

def compileStatements():
    pass

def compileDo():
    pass

def compileLet():
    pass

def compileWhile():
    pass

def compileReturn():
    pass

def compileIf():
    pass

def compileExpression():
    pass

def compileTerm():
    pass

def compileExpressionList():
    pass

def writetoken(token):
    tokentype = token[0]
    tokenname = token[1]
    ret = ''

    if tokentype == 1:
        ret = "<keyword> " + KEYWORD[tokenname] + " </keyword>" 
    elif tokentype == 2:
        ret = "<symbol> " + SYMBOL[tokenname] + " </symbol>" 
    elif tokentype == 3:
        ret = "<identifier> " + tokenname + " </identifier>"
    elif tokentype == 4:
        ret = "<integerConstant> " + str(tokenname) +" </integerConstant>"
    elif tokentype == 5:
        ret = "<stringConstant> " + tokenname + " </stringConstant>"

    return ret