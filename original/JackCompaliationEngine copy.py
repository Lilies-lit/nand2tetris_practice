from JackConstSyntax import *
import JackTockenizer as Tokenizer

'''
(hoge)*の処理

it++
while()
    match-if
    it++

---
<s>
Tab++

Tab--
</s>
'''

def maketab(Tab):
    S = ''
    for i in range(Tab):
        S += '    '
    return S

def writetab(S, tab, o):
    o.write(maketab(tab) + S + "\n")

def wtoken(Token, Tab, o): # write token line, tab
    writetab(o, Tab, Tocknizer.writetoken(Token))

def makexmlline(tag, contents, Tab):
    S = maketab(Tab)
    S += "<" + tag + "> " + contents + " </" + tag + ">\n"
    return S

def compileClass(it, Tab, o):
    writetab('<class>', Tab, o)
    Tab += 1
    writetab('<keyword> class </keyword>', Tab, o)

    T = next(it)
    wtoken(Token, o, Tab) #<identifier> className </identifier>

    T = next(it)
    wtoken(Token, o, Tab) #{
    
    T = next(it)
    while(1):
        if T[0] == C_SYMBOL and T[1] == 1: #}
            break
        
        if T[0] == C_KEYWORD and T[1] in C_CLASSVARDEC:
            C = compileClassVarDec(it, T[1], Tab, o)
            if C > 0:
                return 1
        
        if T[0] == C_KEYWORD and T[1] in C_SUBROUTINE:
            C = compileSubroutine(it, T, Tab, o)
            if C > 0:
                return 1

        if T[0] == C_IDENTIFIER: # subroutineDec -- type -- className
            C = compileSubroutine(it, T, Tab, o)
            if C > 0:
                return 1

    wtoken(Token, o, Tab) #}

    Tab -= 1
    writetab('</class>', Tab, o)


def compileClassVarDec(it, sw, Tab, o):
    writetab('<classVarDec>', Tab, o)
    Tab += 1

    if sw == C_STATIC:
        writetab('<keyword> static </keyword>', Tab, o)
    elif sw == C_FIELD:
        writetab('<keyword> field </keyword>', Tab, o)

    T = next(it) # type
    if not (T[0] == C_IDENTIFIER or (C[0] == C_KEYWORD and C[1] in C_TYPE)):
        return 1

    wtoken(T, Tab, o) # type

    T = next(it) # varName
    wtoken(T, Tab, o)

    T = next(it) # , | ;
    while(1):
        if T[0] == C_SYMBOL and T[1] == C_SEMICOLON:
            break

        wtoken(T, Tab, o) #,
        T = next(it) # varName
        wtoken(T, Tab, o)
        T = next(it)

    wtoken(T, Tab, o) #;
    
    Tab -= 1
    writetab('</classVarDec>', Tab, o)

def compileSubroutine(it, nowT, Tab, o):
    writetab('<subroutineDec>', Tab, o)
    Tab += 1
    wtoken(nowT, Tab, o) # constructor function method void | type
    T = next(it) #subroutineName
    wtoken(T, Tab, o) #<identifier> subroutineName </identifier>

    T = next(it)
    wtoken(T, Tab, o) # (
    
    C = compileParameterList(it, Tab, o)

    wtoken(T, Tab, o) # )

    #subroutineBody
    




    Tab -= 1
    writetab('</subroutineDec>', Tab, o)

def compileParameterList(it, Tab, o):
    writetab('<parameterList>', Tab, o)
    Tab += 1

    T = next(it) #type or )

    while(1):
        if T[0] == C_SYMBOL and T[1] == 3: # )
            break

        wtoken(T, Tab, o) # <type>

        T = next(it) # <identifier> varName </identifier>
        wtoken(T, Tab, o) # <type>

        T = next(it) # ) or ,
        if T[0] == C_SYMBOL and T[1] == 3: # )
            break

        wtoken(T, Tab, o) # <,>

    Tab -= 1
    writetab('</parameterList>', Tab, o)

def compileVarDec(it, Tab, o):
    writetab('<varDec>', Tab, o)
    Tab += 1
    writetab('<symbol> var </symbol>', Tab, o)

    T = next(it) #type
    wtoken(T, Tab, o)

    T = next(it) #varName
    wtoken(T, Tab, o)

    T = next(it) #, or ;
    while(1)
        if T[0] == C_SYMBOL and T[1] = C_SEMICOLON:
            break

        wtoken(T, Tab, o) # ,

        T = next(it)
        wtoken(T, Tab, o) #varName
        
        T = next(it)

    wtoken(T, Tab, o) #;
    Tab -= 1
    writetab('</varDec>', Tab, o)

def compileStatements():
    #let if while do returnでなかったら外に出る
    writetab('<statement>', Tab, o)
    Tab += 1
    T = next(it)
    while(1):
        if not (T[0] == C_KEYWORD and T[1] in C_STATEMENT):
            break

        C = 1
        if T[1] == C_LET:
            C = compileLet()
        elif T[1] == C_DO:
            C = compileDo()
        elif T[1] == C_IF:
            C = compileIf()
        elif T[1] == C_WHILE:
            C = compileWhile()
        elif T[1] == C_RETURN:
            C = compileReturn()


    Tab -= 1
    writetab('</statement>', Tab, o)

def compileDo():
    pass

def compileLet(it , Tab, o):
    writetab('<letStatement>', Tab, o)
    Tab += 1
    writetab('<keyword> let </keyword>', Tab, o)

    T = next(it) #varName
    wtoken(T, Tab, o)

    T = next(it) # [  or =
    #Todo [ ]

    wtoken(T, Tab, o) # =

    C = compileExpression(it, Tab, o)

    T = next(it)      ### for test (右辺1つのtoken)  
    wtoken(T, Tab, o) ### for test


    T = next(it) #;
    wtoken(T, Tab, o) 

    Tab -= 1
    writetab('</letStatement>', Tab, o)

def compileWhile():
    pass

def compileReturn():
    pass

def compileIf():
    writetab('<ifStatement>', Tab, o)
    Tab += 1
    writetab('<keyword> if </keyword>', Tab, o)

    T = next(it) # (
    wtoken(T, Tab, o)

    C = compileExpression(it, Tab, o)

    T = next(it) # )
    wtoken(T, Tab, o)

    T = next(it) #{
    wtoken(T, Tab, o)

    #CALL STATEMENTS
    
    wtoken(T, Tab, o) #}

    #else
    T = next(it) #else
    if T[0] == C_KEYWORD and T[1] == C_ELSE:


    Tab -= 1
    writetab('</ifStatement>', Tab, o)

def compileExpression(it, Tab, o):
    pass

def compileTerm():
    pass

def compileExpressionList():
    pass


