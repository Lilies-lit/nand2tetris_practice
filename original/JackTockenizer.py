# -*- coding: utf-8 -*-
from JackConstSyntax import *


def readword(word):
    # output [*,*,*]
    # 0 .. end
    # -1 .. " Error
    # -2 .. Num error

    if word[0] == '"':
        return [5, word[1:-1]]

    elif word[0] in NUMHEAD:
        try:
            k = int(word)
        except ValueError:
            return -1
        
        if (k < 0) or (32767 < k):
            return -2

        return [4, k]

    elif word in KEYWORD:
        index = KEYWORD.index(word)
        return [1, index]

    elif word in SYMBOL:
        index = SYMBOL.index(word)
        return [2, index]

    else:
        return [3, word] # identifier


def writetoken(token):
    tokentype = token[0]
    tokenname = token[1]
    ret = ''

    if tokentype == 1:
        ret = "<keyword> " + KEYWORD[tokenname] + " </keyword>" 
    elif tokentype == 2:
        if tokenname == 13: # &
            ret = "<symbol> " + "&amp;" + " </symbol>" 
        elif tokenname == 15: # <
            ret = "<symbol> " + "&lt;" + " </symbol>" 
        elif tokenname == 16: # >
            ret = "<symbol> " + "&gt;" + " </symbol>" 
        else:
            ret = "<symbol> " + SYMBOL[tokenname] + " </symbol>"
            
    elif tokentype == 3:
        ret = "<identifier> " + tokenname + " </identifier>"
    elif tokentype == 4:
        ret = "<integerConstant> " + str(tokenname) +" </integerConstant>"
    elif tokentype == 5:
        ret = "<stringConstant> " + tokenname + " </stringConstant>"

    return ret
    


