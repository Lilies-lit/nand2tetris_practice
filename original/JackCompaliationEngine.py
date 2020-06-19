from JackConstSyntax import *
import JackTockenizer as Tokenizer

o = 0
Data = 0

'''
pcはTokenlist(数値化済)の何個目まで呼んだかを表す．
subroutine呼び出し直前で，その文法の先頭のアドレスをさし，
そのroutineを抜けるときにはその文法の最後のアドレス+1を指す．

'''

def maketab(Tab):
    S = ''
    for i in range(Tab):
        S += '    '
    return S

def writetab(S, Tab):
    o.write(maketab(Tab) + S + "\n")

def wtoken(Token, Tab): # write token line, tab
    writetab(Tokenizer.writetoken(Token), Tab)

def makexmlline(tag, contents, Tab):
    S = maketab(Tab)
    S += "<" + tag + "> " + contents + " </" + tag + ">\n"
    return S

def compileFile(inData, outFileName):
    global o
    global Data
    Data = inData

    try:
        o = open(outFileName, 'w')
    except OSError:
        print("file can't open(output)")
        return 1

    pc = 0
    Tab = 0

    while(1):
        T = Data[pc]
        print(T)
        if T[0] == C_KEYWORD and T[1] == C_CLASS:
            pc = compileClass(pc, Tab)
        elif T[0] == 'END':
            break
            
    o.close()
    return 0

def compileClass(pc, Tab):
    writetab('<class>', Tab)
    Tab += 1
    wtoken(Data[pc], Tab)
    pc += 1

    wtoken(Data[pc], Tab) #<identifier> className </identifier>
    pc += 1

    wtoken(Data[pc], Tab) #{
    pc += 1

    while(1):
        T = Data[pc]

        if T[0] == C_SYMBOL and T[1] == 1: #}
            break
        
        elif T[0] == C_KEYWORD and T[1] in C_CLASSVARDEC:
            pc = compileClassVarDec(pc, Tab)
        
        elif T[0] == C_KEYWORD and T[1] in C_SUBROUTINE:
            pc = compileSubroutine(pc, Tab)

    wtoken(Data[pc], Tab) #}
    pc += 1

    Tab -= 1
    writetab('</class>', Tab)
    return pc

def compileClassVarDec(pc, Tab):
    writetab('<classVarDec>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # static | field
    pc += 1

    T = Data[pc]
    if not (T[0] == C_IDENTIFIER or (T[0] == C_KEYWORD and T[1] in C_TYPE)):
        return -1

    wtoken(Data[pc], Tab) # type
    pc += 1

    wtoken(Data[pc], Tab) # varName
    pc += 1 # , | ;

    while(1):
        T = Data[pc]
        if T[0] == C_SYMBOL and T[1] == C_SEMICOLON:
            break

        wtoken(T, Tab) #,
        pc += 1 # varName
        wtoken(Data[pc], Tab)
        pc += 1

    wtoken(Data[pc], Tab) #;
    pc += 1
    
    Tab -= 1
    writetab('</classVarDec>', Tab)
    return pc

def compileSubroutine(pc, Tab):
    writetab('<subroutineDec>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # constructor function method 
    pc += 1

    wtoken(Data[pc], Tab) # void | type
    pc += 1 #subroutineName

    wtoken(Data[pc], Tab) #<identifier> subroutineName </identifier>
    pc += 1

    wtoken(Data[pc], Tab) # (
    pc += 1

    pc = compileParameterList(pc, Tab)

    wtoken(Data[pc], Tab) # )
    pc += 1

    pc = compileSubroutineBody(pc, Tab)
    
    Tab -= 1
    writetab('</subroutineDec>', Tab)

    return pc

def compileSubroutineBody(pc, Tab):
    writetab('<subroutineBody>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # {
    pc += 1

    while(1): #varDec*
        
        if Data[pc][0] != C_KEYWORD:
            break

        if Data[pc][1] != C_VAR:
            break

        pc = compileVarDec(pc, Tab)


    pc = compileStatements(pc, Tab)

    wtoken(Data[pc], Tab) # }
    pc += 1

    Tab -= 1
    writetab('</subroutineBody>', Tab)
    return pc

def compileParameterList(pc, Tab):
    writetab('<parameterList>', Tab)
    Tab += 1

    while(1):
        T = Data[pc]
        if not (T[0] == C_IDENTIFIER or (T[0] == C_KEYWORD and T[1] in C_TYPE)):
            break

        wtoken(Data[pc], Tab) # <type>
        pc += 1 # <identifier> varName </identifier>

        wtoken(Data[pc], Tab) # <identifier> varName </identifier>
        pc += 1

        T = Data[pc]
        if T[0] == C_SYMBOL and T[1] == C_COMMA:
            continue
        else:
            break

    Tab -= 1
    writetab('</parameterList>', Tab)
    return pc

def compileVarDec(pc, Tab):
    writetab('<varDec>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # static or field
    pc += 1

    wtoken(Data[pc], Tab) #type
    pc += 1

    wtoken(Data[pc], Tab) #varName
    pc += 1

    while(1):
        T = Data[pc]
        
        if T[0] == C_SYMBOL and T[1] == C_SEMICOLON:
            break
        
        wtoken(Data[pc], Tab) # ,
        pc += 1

        wtoken(Data[pc], Tab) # varName
        pc += 1
    
    wtoken(Data[pc], Tab) #;
    pc += 1

    Tab -= 1
    writetab('</varDec>', Tab)
    return pc

def compileStatements(pc, Tab):
    #let if while do returnでなかったら外に出る
    writetab('<statements>', Tab)
    Tab += 1

    while(1):
        T = Data[pc]
        
        if not (T[0] == C_KEYWORD and T[1] in C_STATEMENT):
            break

        if T[1] == C_LET:
            pc = compileLet(pc, Tab)
        elif T[1] == C_DO:
            pc = compileDo(pc, Tab)
        elif T[1] == C_IF:
            pc = compileIf(pc, Tab)
        elif T[1] == C_WHILE:
            pc = compileWhile(pc, Tab)
        elif T[1] == C_RETURN:
            pc = compileReturn(pc, Tab)

    Tab -= 1

    writetab('</statements>', Tab)
    return pc

def compileDo(pc, Tab):
    writetab('<doStatement>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # 'do'
    pc += 1

    pc = compileSubroutineCall(pc, Tab)

    wtoken(Data[pc], Tab) # ;
    pc += 1

    Tab -= 1
    writetab('</doStatement>', Tab)
    return pc

def compileLet(pc, Tab):
    writetab('<letStatement>', Tab)
    Tab += 1
    
    wtoken(Data[pc], Tab) # 'let'
    pc += 1

    wtoken(Data[pc], Tab) #varName
    pc += 1

    if Data[pc][0] == C_SYMBOL and Data[pc][1] == 4: #[
        wtoken(Data[pc], Tab) # [
        pc += 1

        pc = compileExpression(pc, Tab)

        wtoken(Data[pc], Tab) # ]
        pc += 1

    wtoken(Data[pc], Tab) # =
    pc += 1

    pc = compileExpression(pc, Tab)

    wtoken(Data[pc], Tab) # ;
    pc += 1

    Tab -= 1
    writetab('</letStatement>', Tab)
    return pc

def compileWhile(pc, Tab):
    writetab('<whileStatement>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) # 'while'
    pc += 1

    wtoken(Data[pc], Tab) # (
    pc += 1

    pc = compileExpression(pc, Tab)

    wtoken(Data[pc], Tab) # )
    pc += 1

    wtoken(Data[pc], Tab) # {
    pc += 1

    pc = compileStatements(pc, Tab)

    wtoken(Data[pc], Tab) # }
    pc += 1

    Tab -= 1
    writetab('</whileStatement>', Tab)
    return pc

def compileReturn(pc, Tab):
    writetab('<returnStatement>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) #<keyword> return </>
    pc += 1

    if not (Data[pc][0] == C_SYMBOL and Data[pc][1] == C_SEMICOLON):
        pc = compileExpression(pc, Tab)

    wtoken(Data[pc], Tab) # ;
    pc += 1

    Tab -= 1
    writetab('</returnStatement>', Tab)
    return pc

def compileIf(pc, Tab):
    writetab('<ifStatement>', Tab)
    Tab += 1
    
    wtoken(Data[pc], Tab) # 'if'
    pc += 1

    wtoken(Data[pc], Tab) # (
    pc += 1

    pc = compileExpression(pc, Tab)

    wtoken(Data[pc], Tab) # )
    pc += 1

    wtoken(Data[pc], Tab) # {
    pc += 1

    pc = compileStatements(pc, Tab)

    wtoken(Data[pc], Tab) # }
    pc += 1

    if Data[pc][0] == C_KEYWORD and Data[pc][1] == C_ELSE:
        wtoken(Data[pc], Tab) # 'else'
        pc += 1

        wtoken(Data[pc], Tab) # {
        pc += 1

        pc = compileStatements(pc, Tab)

        wtoken(Data[pc], Tab) # }
        pc += 1

    Tab -= 1
    writetab('</ifStatement>', Tab)
    return pc

def compileExpression(pc, Tab):
    writetab('<expression>', Tab)
    Tab += 1

    pc = compileTerm(pc, Tab)

    #(op term)*
    while(1):
        T = Data[pc]
        if not (T[0] == C_SYMBOL and T[1] in C_OP):
            break

        wtoken(Data[pc], Tab) # + , - , ... (op)
        pc += 1

        pc = compileTerm(pc, Tab)

    Tab -= 1
    writetab('</expression>', Tab)
    return pc

def compileTerm(pc, Tab):
    writetab('<term>', Tab)
    Tab += 1

    wtoken(Data[pc], Tab) #TEST
    pc += 1

    Tab -= 1
    writetab('</term>', Tab)
    return pc

def compileExpressionList(pc, Tab):
    writetab('<expressionList>', Tab)
    Tab += 1

    # ToDo

    Tab -= 1
    writetab('</expressionList>', Tab)
    return pc

def compileSubroutineCall(pc, Tab):
    wtoken(Data[pc], Tab) # case 1 subroutineName (identifier) or case 2(className| varName)
    pc += 1

    T = Data[pc]
    #case 1 (
    if T[0] == C_SYMBOL and T[1] == 2:
        wtoken(Data[pc], Tab) #(
        pc += 1
        pc = compileExpressionList(pc, Tab)
        wtoken(Data[pc], Tab) # )

    #case 2 .
    elif T[0] == C_SYMBOL and T[1] == C_DOT:
        wtoken(Data[pc], Tab) # .
        pc += 1

        wtoken(Data[pc], Tab) # subroutineName
        pc += 1

        wtoken(Data[pc], Tab) # (
        pc += 1
        pc = compileExpressionList(pc, Tab)
        wtoken(Data[pc], Tab) # )
        pc += 1

    else:
        return -1

    return pc